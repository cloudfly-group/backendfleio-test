from django.utils.translation import ugettext_lazy as _

SEGMENTATION_ID_RANGE = {
    'vlan': (1, 4094),
    'gre': (1, (2 ** 32) - 1),
    'vxlan': (1, (2 ** 24) - 1),
    'geneve': (1, (2 ** 24) - 1),
}

PROVIDER_TYPES = {
    'local': {
        'display_name': _('Local'),
        'require_physical_network': False,
        'require_segmentation_id': False,
    },
    'flat': {
        'display_name': _('Flat'),
        'require_physical_network': True,
        'require_segmentation_id': False,
    },
    'vlan': {
        'display_name': _('VLAN'),
        'require_physical_network': True,
        'require_segmentation_id': True,
    },
    'gre': {
        'display_name': _('GRE'),
        'require_physical_network': False,
        'require_segmentation_id': True,
    },
    'vxlan': {
        'display_name': _('VXLAN'),
        'require_physical_network': False,
        'require_segmentation_id': True,
    },
    'geneve': {
        'display_name': _('Geneve'),
        'require_physical_network': False,
        'require_segmentation_id': True,
    },
    'midonet': {
        'display_name': _('MidoNet'),
        'require_physical_network': False,
        'require_segmentation_id': False,
    },
    'uplink': {
        'display_name': _('MidoNet Uplink'),
        'require_physical_network': False,
        'require_segmentation_id': False,
    },
}
