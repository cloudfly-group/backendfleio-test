from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import viewsets
from rest_framework.decorators import action

from fleio.billing.cart.utils import create_service_for_item
from fleio.billing.models import Order
from fleio.billing.models import OrderItemConfigurableOption
from fleio.billing.models import OrderItemTypes
from fleio.billing.settings import OrderStatus

from fleio.core.drf import StaffOnly
from fleio.core.models import Client
from fleio.core.validation_utils import validate_services_limit
from fleio.openstack.exceptions import APIException

from plugins.domains.configuration import DomainsSettings
from plugins.domains.configuration import DomainsSettingsSerializer
from plugins.domains.custom_fields.validator import CustomFieldsValidator
from plugins.domains.staff.serializers import CheckCustomFieldsSerializer
from plugins.domains.staff.serializers import PriceCyclesSerializer
from plugins.domains.staff.serializers import RegisterDomainSerializer
from plugins.domains.staff.serializers import TLDSerializer
from plugins.domains.staff.serializers import TransferDomainSerializer
from plugins.domains.models.tld import AddonPriceType
from plugins.domains.models.tld import PriceType
from plugins.domains.staff.serializers import AddonPriceCyclesSerializer
from plugins.domains.utils.domain import DomainUtils


class OrderDomainViewSet(viewsets.GenericViewSet):
    permission_classes = (StaffOnly, )

    @action(detail=False, methods=['get'])
    def is_available_for_registration(self, request: Request) -> Response:
        client_id = request.query_params.get('client_id', None)
        client = Client.objects.get(id=client_id)
        domains_settings = DomainsSettings.for_client(client=client)
        domain_name = request.query_params.get('domain_name', None)
        available, error, adjusted_name = DomainUtils.check_if_domains_is_available_for_registration(
            domain_name=domain_name,
            domains_settings=domains_settings,
            skip_whois_check=True,
        )

        if not available:
            return Response(data={
                'error': error,
                'available': False
            })
        else:
            domain_name = adjusted_name

        tld = DomainUtils.get_tld(domain_name)

        if not tld:
            return Response(data={
                'error': _(
                    'Domains {} are not available for registration'.format(
                        DomainUtils.get_tld_name(domain_name)
                    )
                ),
                'available': False
            })

        if not tld.register_product:
            return Response(data={
                'error': _('No price defined for {} domains'.format(tld.name)),
                'available': False
            })

        price_cycles = tld.get_prices_for_type_and_currency(
            price_type=PriceType.register,
            currency=client.currency
        )

        dns_price_cycles = tld.get_addon_prices_for_type_and_currency(
            price_type=AddonPriceType.dns,
            currency=client.currency
        )

        email_price_cycles = tld.get_addon_prices_for_type_and_currency(
            price_type=AddonPriceType.email,
            currency=client.currency
        )

        id_price_cycles = tld.get_addon_prices_for_type_and_currency(
            price_type=AddonPriceType.id,
            currency=client.currency
        )

        client_details = '{}({})\n{}, {}\n{}, {}'.format(
            client.name,
            client.email,
            client.address1,
            client.city,
            client.state,
            client.country
        )

        return Response(data={
            'client_id': client.id,
            'client_details': client_details,
            'available': True,
            'adjusted_name': adjusted_name,
            'prices': PriceCyclesSerializer().to_representation(instance=price_cycles),
            'dns_prices': AddonPriceCyclesSerializer().to_representation(instance=dns_price_cycles),
            'email_prices': AddonPriceCyclesSerializer().to_representation(instance=email_price_cycles),
            'id_prices': AddonPriceCyclesSerializer().to_representation(instance=id_price_cycles),
            'config': DomainsSettingsSerializer().to_representation(instance=domains_settings),
            'tld': TLDSerializer().to_representation(instance=tld),
        })

    @action(detail=False, methods=['get'])
    def check_custom_fields(self, request: Request) -> Response:
        serializer = CheckCustomFieldsSerializer(data=request.query_params)
        if serializer.is_valid(raise_exception=True):
            client_id = serializer.validated_data['client_id']
            client = Client.objects.get(id=client_id)
            missing_fields = False
            missing_fields_labels = []
            if serializer.validated_data['contact_type'] == 'client':
                missing_fields, missing_fields_labels = CustomFieldsValidator.client_has_missing_fields_for_domain(
                    client_id=client.id,
                    domain_name=serializer.validated_data['domain_name'],
                )
            if serializer.validated_data['contact_type'] == 'contact':
                missing_fields, missing_fields_labels = CustomFieldsValidator.contact_has_missing_fields_for_domain(
                    contact_id=serializer.validated_data['contact_id'],
                    domain_name=serializer.validated_data['domain_name'],
                )

            return Response(data={
                'missing_fields': missing_fields,
                'missing_fields_labels': missing_fields_labels,
            })

    @action(detail=False, methods=['post'])
    def register_domain(self, request: Request) -> Response:
        serializer = RegisterDomainSerializer(
            data=request.data['domain'],
            context={'request': self.request},
        )
        if serializer.is_valid(raise_exception=True):
            client = Client.objects.get(id=serializer.validated_data['client'])
            domains_settings = DomainsSettings.for_client(client=client)
            domain_name = serializer.validated_data['name']
            available, error, adjusted_name = DomainUtils.check_if_domains_is_available_for_registration(
                domain_name=domain_name,
                domains_settings=domains_settings,
                skip_whois_check=True,
            )

            if not available:
                Response(
                    data={
                        'detail': error
                    },
                    status=400)
            else:
                domain_name = adjusted_name

            tld = DomainUtils.get_tld(domain_name=domain_name)

            user = client.users.first()
            if not user:
                user = request.user
            order = Order.objects.create(user=user,
                                         client=client,
                                         currency=client.currency,
                                         client_notes='',
                                         status=OrderStatus.pending)
            cycle = tld.register_product.cycles.filter(
                currency=client.currency,
                cycle_multiplier=serializer.validated_data['years'] + 1,
            ).first()

            dns_cycle = tld.dns_option.cycles.filter(
                currency=client.currency,
                cycle_multiplier=serializer.validated_data['years'] + 1,
            ).first() if serializer.validated_data.get('dns_management', False) else None

            email_cycle = tld.email_option.cycles.filter(
                currency=client.currency,
                cycle_multiplier=serializer.validated_data['years'] + 1,
            ).first() if serializer.validated_data.get('email_forwarding', False) else None

            id_cycle = tld.id_option.cycles.filter(
                currency=client.currency,
                cycle_multiplier=serializer.validated_data['years'] + 1,
            ).first() if serializer.validated_data.get('id_protection', False) else None

            plugin_data = dict(serializer.validated_data)
            plugin_data['operation'] = 'register'
            with transaction.atomic():
                order_item = order.items.create(
                    item_type=OrderItemTypes.service,
                    product=tld.register_product,
                    cycle=cycle,
                    fixed_price=cycle.fixed_price,
                    cycle_display=cycle.display_name,
                    plugin_data=plugin_data,
                    name=domain_name,
                    description=_('Domain registration'),
                )

                if dns_cycle:
                    OrderItemConfigurableOption.objects.create(
                        order_item=order_item,
                        option=tld.dns_option,
                        option_value="yes",
                        quantity=1,
                        has_price=True,
                        unit_price=dns_cycle.price,
                        price=dns_cycle.price,
                        setup_fee=0
                    )

                if email_cycle:
                    OrderItemConfigurableOption.objects.create(
                        order_item=order_item,
                        option=tld.email_option,
                        option_value="yes",
                        quantity=1,
                        has_price=True,
                        unit_price=email_cycle.price,
                        price=email_cycle.price,
                        setup_fee=0
                    )

                if id_cycle:
                    OrderItemConfigurableOption.objects.create(
                        order_item=order_item,
                        option=tld.id_option,
                        option_value="yes",
                        quantity=1,
                        has_price=True,
                        unit_price=id_cycle.price,
                        price=id_cycle.price,
                        setup_fee=0
                    )

                if not validate_services_limit():
                    raise APIException(
                        _('License service limit reached. Please check your license'),
                    )

                create_service_for_item(item=order_item)

                return Response(data={
                    'order_id': order.id,
                })

    @action(detail=False, methods=['get'])
    def is_available_for_transfer(self, request: Request) -> Response:
        client_id = request.query_params.get('client_id', None)
        client = Client.objects.get(id=client_id)
        domains_settings = DomainsSettings.for_client(client=client)
        domain_name = request.query_params.get('domain_name', None)
        available, error, adjusted_name = DomainUtils.check_if_domains_is_available_for_transfer(
            domain_name=domain_name,
            domains_settings=domains_settings,
            skip_whois_check=True,
        )

        if not available:
            return Response(data={
                'error': error,
                'available': False
            })
        else:
            domain_name = adjusted_name

        tld = DomainUtils.get_tld(domain_name)

        if not tld:
            return Response(data={
                'error': _(
                    'Domains {} are not available for transfer'.format(
                        DomainUtils.get_tld_name(domain_name)
                    )
                ),
                'available': False
            })

        if not tld.transfer_product:
            return Response(data={
                'error': _('No price defined for {} domains'.format(tld.name)),
                'available': False
            })

        price_cycles = tld.get_prices_for_type_and_currency(
            price_type=PriceType.transfer,
            currency=client.currency
        )

        return Response(data={
            'available': True,
            'adjusted_name': adjusted_name,
            'prices': PriceCyclesSerializer().to_representation(instance=price_cycles),
            'config': DomainsSettingsSerializer().to_representation(instance=domains_settings),
            'tld': TLDSerializer().to_representation(instance=tld),
        })

    @action(detail=False, methods=['post'])
    def transfer_domain(self, request: Request) -> Response:
        serializer = TransferDomainSerializer(data=request.data['domain'])
        if serializer.is_valid(raise_exception=True):
            client = Client.objects.get(id=serializer.validated_data['client'])
            domains_settings = DomainsSettings.for_client(client=client)
            domain_name = serializer.validated_data['name']
            available, error, adjusted_name = DomainUtils.check_if_domains_is_available_for_transfer(
                domain_name=domain_name,
                domains_settings=domains_settings,
                skip_whois_check=True,
            )

            if not available:
                Response(
                    data={
                        'detail': error
                    },
                    status=400)
            else:
                domain_name = adjusted_name

            tld = DomainUtils.get_tld(domain_name=domain_name)

            with transaction.atomic():
                user = client.users.first()
                if not user:
                    user = request.user
                order = Order.objects.create(user=user,
                                             client=client,
                                             currency=client.currency,
                                             client_notes='',
                                             status=OrderStatus.pending)
                cycle = tld.register_product.cycles.filter(
                    currency=client.currency,
                    cycle_multiplier=serializer.validated_data['years'] + 1,
                ).first()
                plugin_data = dict(serializer.validated_data)
                plugin_data['operation'] = 'transfer'
                plugin_data['epp'] = serializer.validated_data['epp']
                order_item = order.items.create(
                    item_type=OrderItemTypes.service,
                    product=tld.transfer_product,
                    cycle=cycle,
                    fixed_price=cycle.fixed_price,
                    cycle_display=cycle.display_name,
                    plugin_data=plugin_data,
                    name=domain_name,
                    description=_('Domain transfer'),
                )

                if not validate_services_limit():
                    raise APIException(
                        _('License service limit reached. Please check your license'),
                    )

                create_service_for_item(item=order_item)

                return Response(data={
                    'order_id': order.id,
                })
