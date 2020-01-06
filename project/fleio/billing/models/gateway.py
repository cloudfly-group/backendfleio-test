import decimal

from jsonfield import JSONField

from django.db import models

from fleio.billing import utils


class GatewayQuerySet(models.QuerySet):
    def enabled(self):
        return self.filter(enabled=True)

    def visible_to_user(self):
        return self.enabled().filter(visible_to_user=True)

    def visible_to_staff(self):
        return self.enabled()


class Gateway(models.Model):
    name = models.CharField(max_length=64, help_text='Gateway name')
    enabled = models.BooleanField(default=False)
    recurring_payments_enabled = models.BooleanField(default=False)
    visible_to_user = models.BooleanField(default=False)
    instructions = models.TextField(max_length=1024, default='')

    fixed_fee = models.DecimalField(decimal_places=2, max_digits=14, default=0.0)
    percent_fee = models.DecimalField(decimal_places=2, max_digits=5, default=0.0)
    module_path = models.CharField(max_length=255)
    module_settings = JSONField(default='{}')
    display_name = models.CharField(max_length=255, blank=True)

    objects = GatewayQuerySet.as_manager()

    @property
    def module(self):
        # FIXME(tomo): Find a way to disable un-importable modules
        gw_app_conf = utils.get_payment_module_by_label(self.name)
        if gw_app_conf:
            mod_path = '{}.{}'.format(gw_app_conf.name, gw_app_conf.label)
            return utils.get_module(mod_path, raise_exception=False)
        else:
            return None

    def log_callback(self, external_id=None, data=None, status=None,
                     error=None, error_info=None, error_code=None):
        return self.gateway_logs.create(external_id=external_id,
                                        data=data,
                                        status=status,
                                        error=error,
                                        error_info=error_info or '',
                                        error_code=error_code or '')

    def get_fee(self, amount: decimal.Decimal) -> decimal.Decimal:
        fee = decimal.Decimal('0.0')
        if self.fixed_fee:
            fee = self.fixed_fee
        if self.percent_fee:
            fee += amount * (self.percent_fee / decimal.Decimal(100))
        fee = utils.cdecimal(fee)  # call cdecimal since we require 2 decimal places for this model
        return fee

    def __str__(self):
        return self.name
