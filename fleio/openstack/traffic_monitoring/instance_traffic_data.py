import logging
from datetime import date
from datetime import datetime
from datetime import timedelta
from decimal import Decimal

from django.utils.translation import ugettext_lazy as _

# minutes approximation for period match
from fleio.openstack.models import NetworkPortTraffic

MINUTES_APPROXIMATION = 5  # type: int
LOG = logging.getLogger(__name__)


class InstanceTrafficType:
    public = 'public'
    private = 'private'

    traffic_type_map = {
        private: _('Private'),
        public: _('Public')
    }


class InstanceTrafficData:
    def __init__(self, start: datetime, end: datetime):
        self.incoming_private = 0
        self.incoming_public = 0

        self.outgoing_private = 0
        self.outgoing_public = 0

        self.total_public = 0
        self.total_private = 0

        self.total = 0

        self.start = start.date()
        self.end = end.date()

        self.price = Decimal()

    def add_traffic(self, port_traffic: NetworkPortTraffic):
        traffic_type = InstanceTrafficType.private if port_traffic.resource.is_private else InstanceTrafficType.public
        if traffic_type not in InstanceTrafficType.traffic_type_map:
            raise Exception('Unsupported traffic type "{}"'.format(traffic_type))

        if not self.period_matches(
            start=port_traffic.start_datetime.date(),
            end=port_traffic.end_datetime.date(),
        ):
            LOG.debug('Period does not match for port traffic, skipping.')
            return

        if traffic_type == InstanceTrafficType.private:
            self.incoming_private += port_traffic.incoming_bytes
            self.outgoing_private += port_traffic.outgoing_bytes

            self.total_private += port_traffic.incoming_bytes + port_traffic.outgoing_bytes

        if traffic_type == InstanceTrafficType.public:
            self.incoming_public += port_traffic.incoming_bytes
            self.outgoing_public += port_traffic.outgoing_bytes

            self.total_public += port_traffic.incoming_bytes + port_traffic.outgoing_bytes

        self.total += port_traffic.incoming_bytes + port_traffic.outgoing_bytes

    def period_matches(self, start: date, end: date) -> bool:
        match = True
        approximation = timedelta(minutes=MINUTES_APPROXIMATION)
        if self.start:
            delta = self.start - start
            match = match and abs(delta) < approximation

        if self.end:
            delta = self.end - end
            match = match and abs(delta) < approximation

        return match
