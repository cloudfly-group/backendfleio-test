from datetime import timedelta
from typing import Optional

from django.db import models

from .network_port_resource import NetworkPortResource


class NetworkPortTrafficTypes:
    per_month = 'month'
    per_billing_cycle = 'cycle'


class NetworkPortTraffic(models.Model):
    incoming_bytes = models.BigIntegerField(default=0)
    incoming_bytes_start = models.BigIntegerField(default=0)
    incoming_bytes_end = models.BigIntegerField(default=0)
    incoming_bytes_accumulation = models.BigIntegerField(default=0)
    last_incoming_metric = models.BigIntegerField(default=0)

    outgoing_bytes = models.BigIntegerField(default=0)
    outgoing_bytes_start = models.BigIntegerField(default=0)
    outgoing_bytes_end = models.BigIntegerField(default=0)
    outgoing_bytes_accumulation = models.BigIntegerField(default=0)
    last_outgoing_metric = models.BigIntegerField(default=0)

    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=64)

    resource = models.ForeignKey(
        NetworkPortResource, on_delete=models.PROTECT, null=False, blank=False, related_name='traffic_data',
    )

    def get_previous(self) -> Optional['NetworkPortTraffic']:
        previous_datetime = self.start_datetime - timedelta(hours=12)
        return NetworkPortTraffic.objects.filter(
            start_datetime__lt=previous_datetime,
            end_datetime__gt=previous_datetime,
            type=self.type,
            resource=self.resource,
        ).first()

    def init_from_previous(self, save_after_init: bool = True):
        previous_traffic = self.get_previous()
        if previous_traffic:
            self.incoming_bytes_start = previous_traffic.incoming_bytes_end
            self.incoming_bytes_end = previous_traffic.incoming_bytes_end
            self.last_incoming_metric = previous_traffic.last_incoming_metric
            self.incoming_bytes_accumulation = previous_traffic.incoming_bytes_accumulation

            self.outgoing_bytes_start = previous_traffic.outgoing_bytes_end
            self.outgoing_bytes_end = previous_traffic.outgoing_bytes_end
            self.last_outgoing_metric = previous_traffic.last_outgoing_metric
            self.outgoing_bytes_accumulation = previous_traffic.outgoing_bytes_accumulation
        else:
            self.last_outgoing_metric = -1
            self.last_incoming_metric = -1

        if save_after_init:
            self.save()

    def add_measures(self, new_measures: dict):
        if 'bytes_in' in new_measures:
            new_bytes_in = int(new_measures['bytes_in'])
            if self.last_incoming_metric > new_bytes_in:
                self.incoming_bytes_accumulation = self.incoming_bytes_end

            self.incoming_bytes_end = new_bytes_in + self.incoming_bytes_accumulation
            if self.last_incoming_metric == -1:
                # first cycle, start from 0 traffic
                self.incoming_bytes_start = self.incoming_bytes_end

            self.last_incoming_metric = new_bytes_in
            self.incoming_bytes = self.incoming_bytes_end - self.incoming_bytes_start

        if 'bytes_out' in new_measures:
            new_bytes_out = int(new_measures['bytes_out'])
            if self.last_outgoing_metric > new_bytes_out:
                self.outgoing_bytes_accumulation = self.outgoing_bytes_end

            self.outgoing_bytes_end = new_bytes_out + self.outgoing_bytes_accumulation
            if self.last_outgoing_metric == -1:
                # first cycle, start from 0 traffic
                self.outgoing_bytes_start = self.outgoing_bytes_end

            self.last_outgoing_metric = new_bytes_out
            self.outgoing_bytes = self.outgoing_bytes_end - self.outgoing_bytes_start
