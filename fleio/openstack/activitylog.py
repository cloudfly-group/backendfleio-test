from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from fleio.activitylog.formatting import logclass_text
from fleio.activitylog.operations import add_request_log, fetch_log_category

from .signals.signals import instance_attach_ips, instance_delete_port, instance_detach_ips, port_created


openstack_log_text = {
    'instance_create': _('User {username} created instance {instance_id}'),
    'port_created': _('Port {port_id} for instance {instance_id} created with ips {ips}'),
    'instance_attach_ips': _('Staff user {username} ({user_id}) assigned IP(s) {ips} to instance {instance_id}'
                             ' via port {port_id} of network {network_id}'),
    'instance_detach_ips': _('Staff user {username} ({user_id}) detached IP(s) {ips} from instance {instance_id} '
                             'via port {port_id} of network {network_id}'),
    'instance_delete_port': _('Staff user {username} ({user_id}) detached IP(s) {ips} from instance {instance_id} '
                              'via port {port_id} of network {network_id}. Port deleted'),
    'staff_delete_instance': _('Staff user {username} ({user_id}) deleted an instance {instance_name} '
                               '({instance_id})'),
    'staff_delete_volume': _('Staff user {username} ({user_id}) deleted a volume {volume_name} ({volume_id})'),
    'staff_delete_flavor': _('Staff user {username} ({user_id}) deleted a flavor {flavor_name} ({flavor_id})'),
    'staff_delete_image': _('Staff user {username} ({user_id}) deleted an image {image_name} ({image_id})'),
    'staff_delete_network': _('Staff user {username} ({user_id}) deleted a network {network_name} ({network_id})'),
    'user_delete_instance': _('User {username} ({user_id}) deleted an instance {instance_name} ({instance_id})'),
    'user_delete_volume': _('User {username} ({user_id}) deleted a volume {volume_name} ({volume_id})'),
    'user_delete_image': _('User {username} ({user_id}) deleted an image {image_name} ({image_id})'),
    'user_delete_network': _('User {username} ({user_id}) deleted a network {network_name} ({network_id})'),
    'user_delete_router': _('User {username} ({user_id}) deleted a router {router_name} ({router_id})'),
    'user_delete_security_group': _('User {username} ({user_id}) deleted a '
                                    'security group {secgroup_name} ({secgroup_id})'),
    'user_delete_floating_ip': _('User {username} ({user_id}) deleted a floating ip '
                                 '{floating_ip} ({floating_ip_id})'),
}

logclass_text.update(openstack_log_text)


@receiver(instance_attach_ips, dispatch_uid='log_instance_attach_ips')
def log_instance_attach_ips(sender, **kwargs):
    add_request_log(fetch_log_category('openstack'), 'instance_attach_ips', 'info', **kwargs)


@receiver(instance_detach_ips, dispatch_uid='log_instance_detach_ips')
def log_instance_detach_ips(sender, **kwargs):
    add_request_log(fetch_log_category('openstack'), 'instance_detach_ips', 'info', **kwargs)


@receiver(instance_delete_port, dispatch_uid='log_instance_delete_port')
def log_instance_delete_port(sender, **kwargs):
    add_request_log(fetch_log_category('openstack'), 'instance_delete_port', 'info', **kwargs)


@receiver(port_created, dispatch_uid='log_port_created')
def log_port_created(sender, **kwargs):
    add_request_log(fetch_log_category('openstack'), 'port_created', 'info', **kwargs)
