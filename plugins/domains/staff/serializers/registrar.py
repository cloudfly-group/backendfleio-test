from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _

from plugins.domains.models import Domain
from plugins.domains.models import Registrar
from plugins.domains.models.domain import DomainStatus
from plugins.domains.utils.domain import DomainUtils


class RegistrarSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.price_domain_id = kwargs.get('price_domain_id', None)
        if self.price_domain_id:
            del kwargs['price_domain_id']

        super().__init__(*args, **kwargs)

    registrar_connector_display = serializers.SerializerMethodField()
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = Registrar
        fields = '__all__'

    @staticmethod
    def get_registrar_connector_display(instance: Registrar):
        return instance.connector.name

    def get_display_name(self, instance: Registrar):
        if self.price_domain_id:
            domain = Domain.objects.filter(id=self.price_domain_id).first()
            if domain:
                prices = DomainUtils.get_domain_registrar_prices(domain=domain, registrar=instance)
                price_for_action = None
                action = None
                if prices:
                    if domain.status == DomainStatus.pending:
                        price_for_action = prices.register_price
                        action = _('register domain ')
                    if domain.status == DomainStatus.pending_transfer:
                        price_for_action = prices.transfer_price
                        action = _('transfer domain')
                    if domain.status == DomainStatus.active:
                        price_for_action = prices.renew_price
                        action = _('renew domain')

                if price_for_action:
                    return _('{} - {} {} {} for {} year(s)').format(
                        instance.name,
                        prices.register_price if domain.status == DomainStatus.pending else prices.renew_price,
                        prices.currency,
                        action,
                        domain.registration_period,
                    )
                else:
                    return _('{} - {}').format(
                        instance.name,
                        _('no prices available')
                    )

        return instance.name
