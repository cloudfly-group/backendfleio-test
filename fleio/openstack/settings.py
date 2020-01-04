import logging

from django.conf import settings

from fleio.conf import options
from fleio.conf.base import ConfigOpts

LOG = logging.getLogger(__name__)

OS_TYPES = (('altlinux', 'Altlinux'),
            ('arch', 'Arch Linux'),
            ('centos', 'CentOS'),
            ('cirros', 'CirrOS'),
            ('debian', 'Debian'),
            ('dos', 'DOS'),
            ('fedora', 'Fedora'),
            ('fedora-atomic', 'Fedora Atomic'),
            ('freebsd', 'Freebsd'),
            ('gnome', 'Gnome'),
            ('macos', 'MacOS'),
            ('mageia', 'Mageia'),
            ('mandrake', 'Mandrake'),
            ('mandriva', 'Mandriva'),
            ('netbsd', 'NetBSD'),
            ('netware', 'Netware'),
            ('openbsd', 'OpenBSD'),
            ('opensuse', 'OpenSUSE'),
            ('rhel', 'RHEL'),
            ('rhl', 'RHL'),
            ('solaris', 'Solaris'),
            ('suse', 'Suse'),
            ('ubuntu', 'Ubuntu'),
            ('windows', 'Windows'),
            )

OS_HYPERVISOR_TYPES = getattr(
    settings, 'OS_HYPERVISOR_TYPES', ('hyperv', 'ironic', 'lxc', 'qemu', 'uml', 'vmware', 'xen', 'kvm', 'lxd', )
)


def get_default_api_value(service):
    """
    Returns the default value for an OpenStack service, ex: compute, identity, etc.

    service: str, the OpenStack service to check against a dict of supported versions
    """

    default_value = settings.FLEIO_API_VERSIONS.get(service)

    if not default_value:
        LOG.debug('Service: {} missing from supported api versions, using default value: None'.format(service))
        return
    else:
        return default_value.get('min_version')


def get_excluded_projects():
    excluded_project_ids = []
    if plugin_settings.HIDE_PROJECTS_AND_API_USERS:
        excluded_project_ids = [plugin_settings.USER_PROJECT_ID]
        if plugin_settings.HIDE_PROJECT_IDS:
            excluded_project_ids = excluded_project_ids + [
                project_id for project_id in plugin_settings.HIDE_PROJECT_IDS.split(',')
            ]

    return excluded_project_ids


class OSConfig(ConfigOpts):
    auth_url = options.URIOpt(label='Keystone auth URL', required=True)
    username = options.StringOpt(default='admin', required=True)
    password = options.StringOpt(encrypted=True, required=True)
    user_domain_id = options.StringOpt(default='default')
    insecure = options.BoolOpt(default=False)
    identity_type = options.StringOpt(default='identity')
    default_role = options.StringOpt(default='', allow_null=True)
    default_interface = options.StringOpt(choices=('admin', 'public', 'private'), default='public')
    user_project_id = options.StringOpt(required=True)
    default_region = options.StringOpt(default='', allow_null=True)
    default_project_name = options.DjangoStringTemplateOpt(default='{{ client.name }} - {{ client.id }}',
                                                           allow_null=False,
                                                           required=True)
    default_project_description = options.DjangoStringTemplateOpt(default='Fleio created for {{ client.name }}',
                                                                  allow_null=False,
                                                                  required=True)
    project_domain_id = options.StringOpt(default='default')
    identity_api_version = options.StringOpt(max_length=6, default=get_default_api_value('identity'))
    compute_api_version = options.StringOpt(default=get_default_api_value('compute'))
    dns_api_version = options.StringOpt(default=get_default_api_value('dns'))
    volume_api_version = options.StringOpt(default=get_default_api_value('volume'))
    volumev2_api_version = options.StringOpt(default=get_default_api_value('volumev2'))
    volumev3_api_version = options.StringOpt(default=get_default_api_value('volumev3'))
    volume_service_type = options.StringOpt(default=settings.OPENSTACK_DEFAULT_VOLUME_SERVICE_TYPE)
    network_api_version = options.StringOpt(default=get_default_api_value('network'))
    image_api_version = options.StringOpt(default=get_default_api_value('image'))
    metric_api_version = options.StringOpt(default=get_default_api_value('metric'))
    container_infra_api_version = options.StringOpt(default=get_default_api_value('container-infra'))
    notifications_url = options.ListOpt(encrypted=True, item_type=options.URIOpt(schemes=('rabbit', 'amqp', 'kombu',
                                                                                          'pika', 'zmq', 'kafka'),
                                                                                 default='rabbit:///',
                                                                                 require_authority=False))
    notifications_topic = options.ListOpt(default=['notifications'])
    notifications_exchange = options.ListOpt(default=['cinder', 'glance', 'keystone', 'neutron', 'nova', 'openstack'])
    notifications_pool = options.StringOpt(default=None, allow_null=True)
    timeout = options.IntegerOpt(min=1, default=60)
    require_valid_ssl = options.BoolOpt(default=False)
    volume_size_increments = options.JsonOpt(allow_null=True)
    notifications_settings_version = options.StringOpt(default='0')

    hide_projects_and_api_users = options.BoolOpt(default=False)
    hide_project_ids = options.StringOpt(default=None, allow_null=True)
    prefix_api_users_with_username = options.BoolOpt(default=False)
    auto_allocated_topology = options.BoolOpt(default=True)
    force_config_drive_for_instance_creation = options.BoolOpt(default=False)

    class Meta:
        section = 'OPENSTACK_PLUGIN'


plugin_settings = OSConfig()
