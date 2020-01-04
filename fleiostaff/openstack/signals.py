# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.dispatch import Signal

staff_delete_instance = Signal(providing_args=['user', 'username', 'request'])
staff_delete_volume = Signal(providing_args=['user', 'username', 'request'])
staff_delete_volume_backup = Signal(providing_args=['user', 'username', 'request'])
staff_delete_flavor = Signal(providing_args=['user', 'username', 'request'])
staff_delete_image = Signal(providing_args=['user', 'username', 'request'])
staff_delete_network = Signal(providing_args=['user', 'username', 'request'])
