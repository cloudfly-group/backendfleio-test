from django.contrib import admin

from fleio.openstack import models


class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'project_id')
    search_fields = ['project_id', 'project_domain_id']
    list_display = ('service', 'project_id', 'project_domain_id', 'disabled')


class OpenstackRoleAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'name')
    search_fields = ['id', 'name']
    list_display = ('id', 'name')


class InstanceAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name', 'region', 'project__project_id']
    list_display = ('id', 'name', 'region', 'status', 'hostId')


class HypervisorAdmin(admin.ModelAdmin):
    list_display = ('id', 'host_name', 'region', 'host_ip', 'memory_mb', 'local_gb',)


class NetworkPortResourceAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'last_check', 'resource_id', 'instance_id', 'region', 'project_id', 'vnic_name', 'found_port_id',
    )


class NetworkPortTrafficAdmin(admin.ModelAdmin):
    list_display = ('id', 'incoming_bytes', 'outgoing_bytes', 'start_datetime', 'end_datetime', 'type', 'resource')


class VolumeTypeToProjectAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'volume_type_id')


class VolumeTypeExtraSpecAdmin(admin.ModelAdmin):
    list_display = ('key', 'volume_type_id')


class SecurityGroupAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'sync_version', 'region', 'project', 'created_at', 'updated_at', 'name', 'description')
    search_fields = ['id', 'name', 'description', 'project__project_id']
    list_display = ('name', 'description', 'project_id', 'id', 'updated_at')


class SecurityGroupRuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'security_group')


class VolumeBackupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'volume', 'project_id')


class VolumeSnapshotAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'volume', 'project_id')


admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.OpenstackRole, OpenstackRoleAdmin)
admin.site.register(models.Hypervisor, HypervisorAdmin)
admin.site.register(models.Instance, InstanceAdmin)
admin.site.register(models.Image, admin.ModelAdmin)
admin.site.register(models.ImageMembers, admin.ModelAdmin)
admin.site.register(models.OpenstackInstanceFlavor, admin.ModelAdmin)
admin.site.register(models.FlavorGroup, admin.ModelAdmin)
admin.site.register(models.FloatingIp, admin.ModelAdmin)
admin.site.register(models.OpenstackRegion, admin.ModelAdmin)
admin.site.register(models.Network, admin.ModelAdmin)
admin.site.register(models.NetworkPortResource, NetworkPortResourceAdmin)
admin.site.register(models.NetworkPortTraffic, NetworkPortTrafficAdmin)
admin.site.register(models.NetworkRbac, admin.ModelAdmin)
admin.site.register(models.NetworkTag, admin.ModelAdmin)
admin.site.register(models.Subnet, admin.ModelAdmin)
admin.site.register(models.SubnetPool, admin.ModelAdmin)
admin.site.register(models.Port, admin.ModelAdmin)
admin.site.register(models.Router, admin.ModelAdmin)
admin.site.register(models.SecurityGroup, SecurityGroupAdmin)
admin.site.register(models.SecurityGroupRule, SecurityGroupRuleAdmin)
admin.site.register(models.Volume, admin.ModelAdmin)
admin.site.register(models.VolumeAttachments, admin.ModelAdmin)
admin.site.register(models.VolumeType, admin.ModelAdmin)
admin.site.register(models.QoSSpec, admin.ModelAdmin)
admin.site.register(models.VolumeTypeToProject, VolumeTypeToProjectAdmin)
admin.site.register(models.VolumeTypeExtraSpec, VolumeTypeExtraSpecAdmin)
admin.site.register(models.VolumeBackup, VolumeBackupAdmin)
admin.site.register(models.VolumeSnapshot, VolumeSnapshotAdmin)
admin.site.register(models.ClusterTemplate, admin.ModelAdmin)
admin.site.register(models.Cluster, admin.ModelAdmin)
