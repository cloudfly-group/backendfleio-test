from __future__ import unicode_literals

from fleio.core.utils import RandomId
from fleio.openstack.models import Project
from fleio.openstack.projects.serializers import ProjectSyncSerializer
from fleio.openstack.sync.handler import BaseHandler


class ProjectSyncHandler(BaseHandler):
    serializer_class = ProjectSyncSerializer
    version_field = 'sync_version'

    def serialize(self, data, region, timestamp):
        db_project = Project.objects.filter(project_id=data.id).first()
        project_id = RandomId('openstack.Project')() if db_project is None else db_project.id
        service_id = None if db_project is None or db_project.service is None else db_project.service.id
        project_data = {
            'id': project_id,
            'service': service_id,
            'project_id': data.id,
            'project_domain_id': data.domain_id,
            'disabled': not data.enabled,
            'name': data.name if data.name else None,
            'description': data.description if data.description else None,
            'is_domain': data.is_domain,
            self.version_field: self.get_version(timestamp)
        }

        return project_data
