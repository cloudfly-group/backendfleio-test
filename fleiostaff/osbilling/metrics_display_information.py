from django.conf import settings
from django.utils.translation import ugettext_lazy as _


# Help text to display below each metric on pricing rules creation
METRICS_HELP_TEXT = {
    'storage.objects.incoming.bytes': _('Total incoming traffic in Gigabytes per billing cycle. Price is per Gigabyte'),
    'storage.objects.outgoing.bytes': _('Total outgoing traffic in Gigabytes per billing cycle. Price is per Gigabyte'),
    'storage.api.requests': _('Total number of API requests during a month. Price is per request-month'),
    'storage.objects': _('The average number of objects in a month is computed. Price is per object-month'),
    'storage.objects.size': _('The average size used in a month. Price is per Gigabyte-month'),
    'storage.objects.containers': _('Average number of containers during a month. Price is per container-month'),
    'bandwidth': _('Total number of Gigabytes transferred on a Layer 3 networking setup'),
    'ip.floating': _('The average number of Floating IPs is computed during a month. Price is per IP-month'),
    'incoming_public_traffic': _('Total number of Gigabytes incoming on public IP addresses'),
    'incoming_private_traffic': _('Total number of Gigabytes incoming on private IP addresses'),
    'outgoing_public_traffic': _('Total number of Gigabytes outgoing on public IP addresses'),
    'outgoing_private_traffic': _('Total number of Gigabytes outgoing on private IP addresses'),
    'total_public_traffic': _('Total number of Gigabytes transferred on public IP addresses'),
    'total_private_traffic': _('Total number of Gigabytes transferred on private IP addresses'),
    'total_traffic': _('Total number of Gigabytes transferred on all IP addresses'),

}

OVERWRITE_METRICS_HELP_TEXT = getattr(settings, 'METRICS_HELP_TEXT', {})

METRICS_HELP_TEXT = dict(METRICS_HELP_TEXT, **OVERWRITE_METRICS_HELP_TEXT)

# Display name for each metric on pricing rules creation
METRICS_DISPLAY_NAME = {
    'storage.objects.incoming.bytes': _('Incoming traffic'),
    'storage.objects.outgoing.bytes': _('Outgoing traffic'),
    'storage.api.requests': _('API request'),
    'storage.objects': _('Objects'),
    'storage.objects.size': _('Object size in GB'),
    'storage.objects.containers': _('Containers'),
    'radosgw.api.requests': _('API request'),
    'radosgw.objects': _('Objects'),
    'radosgw.objects.size': _('Object size in GB'),
    'radosgw.objects.containers': _('Containers'),
    'bandwidth': _('Project traffic'),
    'ip.floating': _('Floating IPs'),
    'incoming_public_traffic': _('Incoming public traffic'),
    'incoming_private_traffic': _('Incoming private traffic'),
    'outgoing_public_traffic': _('Outgoing public traffic'),
    'outgoing_private_traffic': _('Outgoing private traffic'),
    'total_public_traffic': _('Total public traffic'),
    'total_private_traffic': _('Total private traffic'),
    'total_traffic': _('Total traffic'),

}

OVERWRITE_METRICS_DISPLAY_NAME = getattr(settings, 'METRICS_DISPLAY_NAME', {})

METRICS_DISPLAY_NAME = dict(METRICS_DISPLAY_NAME, **OVERWRITE_METRICS_DISPLAY_NAME)
