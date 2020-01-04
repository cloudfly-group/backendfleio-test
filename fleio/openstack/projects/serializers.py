from __future__ import unicode_literals

from rest_framework import serializers

from fleio.openstack.models import Project


class ProjectSyncSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'
        extra_kwargs = {'id': {'validators': list()}}
