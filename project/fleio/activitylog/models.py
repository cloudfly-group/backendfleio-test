import logging

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField

from fleio.activitylog.formatting import logclass_text, partial_format

LOG = logging.getLogger(__name__)


@python_2_unicode_compatible
class LogCategory(models.Model):
    name = models.CharField(max_length=16, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class LogClass(models.Model):
    LOG_TYPE = (
        ('info', _('info')),
        ('error', _('error')),
    )
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=8, choices=LOG_TYPE, default='info')
    category = models.ForeignKey(LogCategory, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'type')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Log(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    ip = models.GenericIPAddressField(null=True, blank=True)
    log_class = models.ForeignKey(LogClass, on_delete=models.CASCADE)
    parameters = JSONField(null=True, blank=True)

    def __str__(self):
        text = logclass_text.get(
            self.log_class.name, 'No display text found for log class "{}"'.format(self.log_class.name)
        )

        if 'impersonator' in self.parameters:
            # NOTE: we force conversion to str here since _ returns an object that can be converted to string
            # but cannot be added to a string
            text += str(_(' (Impersonated by {impersonator} ({impersonator_id}))'))

        formatted_text, has_all_params = partial_format(
            input_string=str(text), **self.parameters,
        )

        if not has_all_params:
            LOG.debug('Not all parameters for log class {} specified.'.format(self.log_class.name))

        return str(formatted_text)
