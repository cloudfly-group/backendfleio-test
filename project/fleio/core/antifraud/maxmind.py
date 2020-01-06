import logging
import hashlib
import pycountry
from collections import OrderedDict

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

try:
    from minfraud import Client
    from minfraud import errors
except ImportError:
    Client = None
    errors = None

from fleio.core.antifraud.antifraud import FraudResultStatus
from fleio.core.plugins.plugin_dispatcher import plugin_dispatcher

LOG = logging.getLogger(__name__)


class DispositionResult:
    ACCEPT = 'accept'
    MANUAL_REVIEW = 'manual_review'
    REJECT = 'reject'


class FleioMaxMind:
    def __init__(self, timeout=30):
        self.timeout = timeout
        self.maxclient = self.get_client(timeout)

    @staticmethod
    def get_client(timeout) -> Client or None:
        maxmind_clientid = getattr(settings, 'MAXMIND_CLIENTID', None)
        maxmind_license = getattr(settings, 'MAXMIND_LICENSE', None)
        if maxmind_clientid is not None and Client is not None and maxmind_license is not None:
            return Client(account_id=settings.MAXMIND_CLIENTID,
                          license_key=settings.MAXMIND_LICENSE,
                          timeout=timeout)
        elif Client is None:
            LOG.warning('Maxmind minfraud python module is not installed')
        else:
            LOG.debug('MAXMIND_CLIENTID and MAXMIND_LICENSE not found in settings')
            return None

    @staticmethod
    def find_country_state(country_code, state_name):
        try:
            for subdiv in pycountry.subdivisions.get(country_code=country_code):
                if subdiv.name.lower() == state_name.lower():
                    return subdiv.code.split('{}-'.format(country_code))[1]
        except KeyError:
            return None
        return None

    def get_transaction_from_order(self, order):
        trans_device = order.metadata
        trans_account = {'user_id': '{}'.format(order.user.pk),
                         'username_md5': hashlib.md5(order.user.username.encode('utf8')).hexdigest()}
        trans_email = {'address': hashlib.md5(order.user.email.encode('utf8')).hexdigest(),
                       'domain': order.user.email.split('@')[1]}
        region_code = self.find_country_state(order.client.country, order.client.state)
        trans_billing = {'first_name': order.client.first_name,
                         'last_name': order.client.last_name,
                         'company': order.client.company,
                         'address': order.client.address1,
                         'address_2': order.client.address2,
                         'city': order.client.city,
                         'region': region_code,
                         'country': order.client.country,
                         'postal': order.client.zip_code,
                         'phone_number': order.client.phone}
        max_trans = {'device': trans_device,
                     'account': trans_account,
                     'email': trans_email}
        if trans_billing is not None:
            max_trans['billing'] = trans_billing
        return max_trans

    @staticmethod
    def get_fraud_results_from_insights(insights_result):
        """Get results from maxmind insights"""
        result = OrderedDict()
        if insights_result.disposition and insights_result.disposition.action:
            result['Disposition action'] = insights_result.disposition.action
            result['Disposition reason'] = insights_result.disposition.reason
        # Billing address
        if hasattr(insights_result, 'billing_address'):
            result['Distance from IP to address'] = insights_result.billing_address.distance_to_ip_location
            result['IP is in country of address'] = insights_result.billing_address.is_in_ip_country
            result['Postal code is in city'] = insights_result.billing_address.is_postal_in_city
            result['Address latitude'] = insights_result.billing_address.latitude
            result['Address longitude'] = insights_result.billing_address.longitude
        # Email result
        if hasattr(insights_result, 'email'):
            result['Email first seen'] = insights_result.email.first_seen
            result['Free email provider'] = insights_result.email.is_free
            result['Email is high risk'] = insights_result.email.is_high_risk
        # IP address
        if hasattr(insights_result, 'ip_address'):
            result['IP country'] = insights_result.ip_address.country.names.get('en')
            result['IP country is high risk'] = insights_result.ip_address.country.is_high_risk
            result['IP country ISO code'] = insights_result.ip_address.country.iso_code
        if hasattr(insights_result, 'traits'):
            if 'autonomous_system_number' in insights_result.traits:
                result['Autonomus System Number'] = insights_result.traits.get('autonomous_system_number')
                result['Autonomus System Organization'] = insights_result.traits.get('autonomous_system_organization')
                result['ISP'] = insights_result.traits.get('isp')
                result['Organization'] = insights_result.traits.get('organization')
                result['IP address'] = insights_result.traits.get('ip_address')
        result['Risk score'] = insights_result.risk_score
        return result

    @staticmethod
    def get_fraud_results_from_score(score_result):
        """Get results from maxmind score"""
        result = OrderedDict()
        if score_result.disposition and score_result.disposition.action:
            result['Disposition action'] = score_result.disposition.action
            result['Disposition reason'] = score_result.disposition.reason
        result['Risk score'] = score_result.risk_score
        result['IP risk score'] = score_result.ip_address.risk
        if score_result.warnings:
            for warn in score_result.warnings:
                result['Warning'] = warn
        return result

    def check_order(self, order):
        max_transaction = self.get_transaction_from_order(order=order)
        manual_review_score = getattr(order.client.billing_settings, 'maxmind_manual_review_score', 30)
        maxmind_fraud_score = getattr(order.client.billing_settings, 'maxmind_fraud_score', 60)
        insights_enabled = getattr(order.client.billing_settings, 'enable_maxmind_insights', True)
        try:
            if insights_enabled:
                max_score = self.maxclient.insights(transaction=max_transaction)
            else:
                max_score = self.maxclient.score(transaction=max_transaction)
        except errors.InvalidRequestError as e:
            LOG.exception(e)
            return FraudResultStatus.ACCEPT
        else:
            # Add fraud check results to order as key value pairs
            if insights_enabled:
                order.fraud_check_result = self.get_fraud_results_from_insights(max_score)
            else:
                order.fraud_check_result = self.get_fraud_results_from_score(max_score)
            order.save(update_fields=['fraud_check_result'])
            # Check disposition (custom maxmind rules):
            if max_score.disposition and max_score.disposition.action is not None:
                if max_score.disposition.action == DispositionResult.ACCEPT:
                    return FraudResultStatus.ACCEPT
                elif max_score.disposition.action == DispositionResult.MANUAL_REVIEW:
                    plugin_dispatcher.call_function(
                        'todo',
                        'create_todo',
                        title=_('Manual review needed for order {}').format(order),
                        description=_('Order {} may be fraudulent. Manual review is needed.').format(order),
                    )
                    return FraudResultStatus.MANUAL_REVIEW
                elif max_score.disposition.action == DispositionResult.REJECT:
                    plugin_dispatcher.call_function(
                        'todo',
                        'create_todo',
                        title=_('Order {} rejected').format(order),
                        description=_('Order {} may be fraudulent. Manual review is needed.').format(order),
                    )
                    return FraudResultStatus.REJECT

            # Check main risk score
            elif max_score.risk_score >= manual_review_score < maxmind_fraud_score:
                return FraudResultStatus.MANUAL_REVIEW
            elif max_score.risk_score >= maxmind_fraud_score:
                return FraudResultStatus.REJECT
            return FraudResultStatus.ACCEPT
