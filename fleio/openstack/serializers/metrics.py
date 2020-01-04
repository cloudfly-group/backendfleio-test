from __future__ import unicode_literals

import logging
import datetime

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

LOG = logging.getLogger(__name__)


class MeasuresSerializer(serializers.Serializer):
    METRIC_CHOICES = [('cpu_util', _('CPU Utilization')),
                      ('interface_traffic', 'Interface Traffic')]
    hours = serializers.ChoiceField(write_only=True, required=True, choices=[1, 24, 168, 720])
    metric = serializers.ChoiceField(write_only=True, required=True, choices=METRIC_CHOICES)

    def to_internal_value(self, data):
        value = super(MeasuresSerializer, self).to_internal_value(data)
        value['period_end'] = datetime.datetime.utcnow()
        value['period_start'] = datetime.datetime.utcnow() - datetime.timedelta(hours=value['hours'])
        hours_to_granularity = {1: 300, 24: 300, 168: 1800, 720: 3600}
        value['granularity'] = hours_to_granularity[value['hours']]
        return value
