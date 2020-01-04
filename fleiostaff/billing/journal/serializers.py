from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from fleio.billing.gateways.utils import get_transaction_actions
from fleio.billing.models import Journal
from fleio.billing.models.journal_sources import JournalSources
from fleio.core.clients.serializers import ClientMinSerializer
from fleiostaff.billing.transactions.serializers import StaffTransactionSerializer
from fleiostaff.core.users.serializers import StaffUserSerializer


class JournalDirections:
    """Used for representation only"""
    incoming = 'incoming'
    outgoing = 'outgoing'
    internal = 'internal'

    choices = (incoming, _('Incoming'),
               outgoing, _('Outgoing'),
               internal, _('Internal'))


class StaffJournalDetailsSerializer(serializers.ModelSerializer):
    source_name = serializers.CharField(read_only=True, max_length=255)
    destination_name = serializers.CharField(read_only=True, max_length=255)
    direction = serializers.ChoiceField(read_only=True, choices=JournalDirections.choices)
    transaction = StaffTransactionSerializer(read_only=True)
    needs_capture = serializers.SerializerMethodField()
    client = serializers.SerializerMethodField()
    is_refund = serializers.ReadOnlyField()
    user = StaffUserSerializer()

    class Meta:
        model = Journal
        fields = '__all__'

    @staticmethod
    def get_needs_capture(model: Journal):
        if model.transaction:
            actions = get_transaction_actions(model.transaction)
            for action in actions:
                if action.get('name') == 'capture':
                    return True
        return False

    @staticmethod
    def get_source_name(obj: Journal):
        if obj.user:
            user_details = obj.user.get_full_name() or obj.user.username
        else:
            # Note: We should find a better way to deal with items where related user was deleted
            user_details = _('Unknown user')

        if obj.source == JournalSources.transaction:
            if obj.destination == JournalSources.invoice:
                if obj.invoice:
                    return obj.invoice.client.long_name
        elif obj.source == JournalSources.invoice:
            if obj.is_refund:
                if obj.destination == JournalSources.credit:
                    return _('Refund to credit')
                elif obj.destination == JournalSources.transaction:
                    return obj.invoice.client.long_name
                else:
                    return _('Refund')
        elif obj.source == JournalSources.credit:
            return obj.client_credit.client.long_name
        elif obj.source == JournalSources.staff and obj.destination == JournalSources.credit:
            return _('{} added credit').format(user_details)
        return JournalSources.sources_map.get(obj.source)

    @staticmethod
    def get_destination_name(obj: Journal):
        if obj.user:
            user_details = obj.user.get_full_name() or obj.user.username
        else:
            # Note: We should find a better way to deal with items where related user was deleted
            user_details = _('Unknown user')

        if obj.destination == JournalSources.credit:
            return obj.client_credit.client.long_name
        elif obj.destination == JournalSources.staff:
            if obj.source == JournalSources.credit:
                return _('{} removed credit').format(user_details)
        elif obj.destination == JournalSources.invoice:
            return _('Invoice payment')
        elif obj.destination == JournalSources.settlement:
            return _('Auto settled service usage')
        elif obj.destination == JournalSources.transaction:
            return _('Refund through gateway')
        return JournalSources.sources_map.get(obj.destination)

    def to_representation(self, journal: Journal):
        repres = super(StaffJournalDetailsSerializer, self).to_representation(journal)
        repres['source_info'] = {'name': JournalSources.sources_map.get(journal.source)}
        repres['destination_info'] = {'name': JournalSources.sources_map.get(journal.destination)}

        if journal.user:
            user_details = journal.user.get_full_name() or journal.user.username
        else:
            # Note: We should find a better way to deal with items where related user was deleted
            user_details = _('Unknown user')

        if journal.source == JournalSources.transaction:
            if journal.destination == JournalSources.invoice:
                if journal.invoice:
                    repres['source_info'] = {'name': journal.invoice.client.long_name,
                                             'transaction': journal.transaction.external_id}
                    destination_info_name = _('Invoice payment')
                    repres['destination_info'] = {'name': destination_info_name,
                                                  'invoice': journal.invoice.pk}
                    repres['direction'] = JournalDirections.incoming
                else:
                    repres['source_info'] = {'name': journal.transaction.gateway.display_name,
                                             'transaction': journal.transaction.external_id}
                    repres['destination_info'] = {'name': _('Payment for missing invoice'),
                                                  'invoice': None}
                    repres['direction'] = JournalDirections.incoming
            elif journal.destination == JournalSources.credit:
                repres['source_info'] = {'name': journal.client_credit.client.long_name,
                                         'transaction': journal.transaction.external_id}
                repres['destination_info'] = {'name': _('Add to credit'),
                                              'invoice': journal.invoice_id}
                repres['direction'] = JournalDirections.incoming
        elif journal.source == JournalSources.invoice:
            if journal.is_refund:
                if journal.destination == JournalSources.credit:
                    repres['source_info'] = {'name': journal.client_credit.client.long_name}
                    repres['destination_info'] = {'name': _('Refund from invoice to credit'),
                                                  'invoice': journal.invoice_id}
                    repres['direction'] = JournalDirections.internal
                elif journal.destination == JournalSources.transaction:
                    repres['source_info'] = {'name': journal.invoice.client.long_name,
                                             'invoice': journal.invoice.pk}
                    repres['destination_info'] = {'name': _('Refund through gateway'),
                                                  'transaction': journal.transaction.external_id}
                    repres['direction'] = JournalDirections.outgoing
                elif journal.destination == JournalSources.external:
                    repres['source_info'] = {'name': journal.invoice.client.long_name,
                                             'invoice': journal.invoice.pk}
                    repres['destination_info'] = {'name': _('External refund')}
                    repres['direction'] = JournalDirections.outgoing
                else:
                    repres['source_info'] = {'name': journal.invoice.client.long_name,
                                             'invoice': journal.invoice.pk}
                    repres['destination_info'] = {'name': _('Refund')}
                    repres['direction'] = JournalDirections.outgoing
            elif journal.destination == JournalSources.credit:
                repres['source_info'] = {'name': journal.client_credit.client.long_name}
                repres['destination_info'] = {'name': _('Add to credit'),
                                              'invoice': journal.invoice_id}
                repres['direction'] = JournalDirections.internal
            else:
                repres['source_info'] = {'name': journal.invoice.client.long_name}
                repres['destination_info'] = {'name': _('Refund')}
                repres['direction'] = JournalDirections.outgoing
        elif journal.source == JournalSources.credit:
            repres['source_info'] = {'name': journal.client_credit.client.long_name}
            if journal.destination == JournalSources.invoice:
                if journal.invoice and journal.invoice.is_credit_invoice():
                    repres['destination_info'] = {'name': _('Credit withdraw after refund')}
                    repres['direction'] = JournalDirections.outgoing
                else:
                    repres['destination_info'] = {'name': _('Invoice payment from credit'),
                                                  'invoice': journal.invoice.pk}
                    repres['direction'] = JournalDirections.internal
            elif journal.destination == JournalSources.transaction:
                if journal.is_refund:
                    repres['destination_info'] = {'name': _('Refund from credit through gateway'),
                                                  'transaction': journal.transaction.external_id}
                    repres['direction'] = JournalDirections.outgoing
                else:
                    repres['destination_info'] = {'name': JournalSources.sources_map.get(journal.destination)}
                    repres['direction'] = JournalDirections.internal
            elif journal.destination == JournalSources.staff:
                repres['destination_info'] = {'name': _('{} removed credit').format(user_details)}
                repres['direction'] = JournalDirections.internal
            elif journal.destination == JournalSources.settlement:
                repres['destination_info'] = {'name': _('Auto settled usage from credit')}
                repres['direction'] = JournalDirections.internal
            else:
                repres['destination_info'] = {'name': JournalSources.sources_map.get(journal.destination)}
                repres['direction'] = JournalDirections.internal
        elif journal.source == JournalSources.staff:
            if journal.destination == JournalSources.credit:
                repres['source_info'] = {'name': journal.client_credit.client.long_name}
                if journal.user:
                    user_who_added_credit = user_details
                else:
                    user_who_added_credit = 'Staff'
                repres['destination_info'] = {'name': _('{} added credit').format(user_who_added_credit)}
                repres['direction'] = JournalDirections.internal
            else:
                repres['source_info'] = {'name': JournalSources.sources_map.get(journal.source)}
                repres['destination_info'] = {'name': JournalSources.sources_map.get(journal.destination)}
                repres['direction'] = JournalDirections.internal
        else:
            repres['source_info'] = {'name': JournalSources.sources_map.get(journal.source)}
            repres['destination_info'] = {'name': JournalSources.sources_map.get(journal.destination)}
            repres['direction'] = JournalDirections.internal
        return repres

    @staticmethod
    def get_client(obj):
        if obj.invoice:
            return ClientMinSerializer().to_representation(instance=obj.invoice.client)
        elif obj.client_credit:
            return ClientMinSerializer().to_representation(instance=obj.client_credit.client)
        else:
            return None
