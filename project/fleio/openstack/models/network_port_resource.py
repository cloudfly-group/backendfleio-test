from django.db import models

from fleio.openstack.models import Instance
from .network import Network
from .network_port import Port
from .network_subnet import Subnet
from .region import OpenstackRegion


class NetworkPortResource(models.Model):
    """
    Defines association between a gnocchi resource and an openstack port.
    """
    last_check = models.DateTimeField(null=True, blank=True)  # last resource check
    instance_id = models.CharField(max_length=255, db_index=True)  # openstack instance id from gnocchi resource
    resource_id = models.CharField(max_length=255, db_index=True)  # gnocchi resource id
    vnic_name = models.CharField(max_length=256)  # vnic name from gnocchi resource
    found_port_id = models.CharField(max_length=255, db_index=True, null=True)  # port id resolved based on vnic name
    project_id = models.CharField(max_length=255, db_index=True, null=True, blank=True)  # openstack instance project

    port = models.OneToOneField(Port, on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey(OpenstackRegion, on_delete=models.SET_NULL, null=True, blank=True)
    network = models.ForeignKey(Network, null=True, blank=True, on_delete=models.PROTECT, related_name='port_resources')
    subnet = models.ForeignKey(Subnet, null=True, blank=True, on_delete=models.PROTECT, related_name='port_resources')
    existing_instance = models.ForeignKey(
        Instance, null=True, blank=True, on_delete=models.SET_NULL, related_name='port_resources',
    )
    # is private defaults to false since it is preferred to mark unknown ports as public
    is_private = models.BooleanField(default=False)
