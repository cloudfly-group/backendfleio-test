from django.dispatch import Signal

instance_create = Signal(providing_args=['user', 'username', 'instance_id', 'request'])
instance_delete = Signal(providing_args=['user', 'instance_id', 'request'])
instance_stop = Signal(providing_args=['user', 'instance_id', 'request'])
instance_start = Signal(providing_args=['user', 'instance_id', 'request'])
instance_restart = Signal(providing_args=['user', 'instance_id', 'request'])
instance_boot_from_iso = Signal(providing_args=['instance_id', 'is_new_instance'])

instance_attach_ips = Signal(providing_args=['user', 'username', 'port_id', 'instance_id', 'ips'])
instance_detach_ips = Signal(providing_args=['user', 'username', 'port_id', 'instance_id', 'ips'])
instance_delete_port = Signal(providing_args=['user', 'username', 'port_id', 'instance_id', 'ips'])

port_created = Signal(providing_args=['port_id', 'instance_id', 'ips'])

user_delete_instance = Signal(providing_args=['user', 'username', 'request'])
user_delete_volume = Signal(providing_args=['user', 'username', 'request'])
user_delete_image = Signal(providing_args=['user', 'username', 'request'])
user_delete_network = Signal(providing_args=['user', 'username', 'request'])
user_delete_router = Signal(providing_args=['user', 'username', 'request'])
user_delete_security_group = Signal(providing_args=['user', 'username', 'request'])
user_delete_floating_ip = Signal(providing_args=['user', 'username', 'request'])

openstack_error = Signal(providing_args=['event_type', 'event_info', 'payload', 'region', 'timestamp', ])
