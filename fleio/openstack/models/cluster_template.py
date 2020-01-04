from django.db import models


class ClusterTemplate(models.Model):
    id = models.CharField(max_length=36, unique=True, primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    floating_ip_enabled = models.BooleanField(default=False)
    master_flavor_id = models.CharField(max_length=255, null=True, blank=True)
    insecure_registry = models.CharField(max_length=1024, null=True, blank=True, default=None)
    no_proxy = models.CharField(max_length=1024, null=True, blank=True, default=None)
    https_proxy = models.CharField(max_length=1024, null=True, blank=True, default=None)
    http_proxy = models.CharField(max_length=1024, null=True, blank=True, default=None)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    tls_disabled = models.BooleanField(default=False)
    keypair_id = models.CharField(max_length=255, null=True, blank=True)
    public = models.BooleanField(default=False)
    labels = models.CharField(max_length=1024, blank=True, null=True)
    docker_volume_size = models.IntegerField(default=25, null=True)
    server_type = models.CharField(max_length=10)
    external_network_id = models.CharField(max_length=255, null=True, blank=True)
    fixed_subnet = models.CharField(max_length=255, null=True, blank=True)
    fixed_network = models.CharField(max_length=255, null=True, blank=True)
    dns_nameserver = models.CharField(max_length=255, null=True, blank=True)
    coe = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    flavor_id = models.CharField(max_length=255, null=True, blank=True)
    master_lb_enabled = models.BooleanField(default=False)
    cluster_distro = models.CharField(max_length=255, null=True, blank=True)
    image_id = models.CharField(max_length=255, null=True, blank=True)
    volume_driver = models.CharField(max_length=255, null=True, blank=True)
    docker_storage_driver = models.CharField(
        max_length=255, null=True, blank=True, default='devicemapper'
    )
    project = models.ForeignKey(
        'openstack.Project', db_constraint=False, null=True, blank=True, on_delete=models.SET_NULL,
        to_field='project_id'
    )
    network_driver = models.CharField(max_length=255, null=True, blank=True)
    apiserver_port = models.IntegerField(null=True)
    registry_enabled = models.BooleanField(default=False)
    region = models.CharField(max_length=128)
    sync_version = models.BigIntegerField(default=0)

    objects = models.Manager

    def __str__(self):
        return self.name if self.name else self.id
