import logging

from fleio.core.utils import RandomId

from fleio.openstack.models import Project
from fleio.openstack.project import Project as OpenstackProject
from fleio.openstack.projects.sync_handlers import ProjectSyncHandler

LOG = logging.getLogger(__name__)


class ProjectEventHandler(ProjectSyncHandler):
    def __init__(self):
        self.event_handlers = {
            'identity.project.created': self.create_or_update,
            'identity.project.updated': self.create_or_update,
            'identity.project.deleted': self.delete
        }

    def serialize(self, data, region, timestamp):
        try:
            openstack_project_id = data['resource_info']
            openstack_project = OpenstackProject.with_admin_session(project_id=openstack_project_id).api_project
            db_project = Project.objects.filter(project_id=openstack_project_id).first()
            project_id = RandomId('openstack.Project')() if db_project is None else db_project.id
            service_id = None if db_project is None or db_project.service is None else db_project.service.id
            project_data = {
                'id': project_id,
                'service': service_id,
                'project_id': openstack_project_id,
                'project_domain_id': openstack_project.domain_id,
                'disabled': not openstack_project.enabled,
                'name': openstack_project.name if openstack_project.name else None,
                'description': openstack_project.description if openstack_project.description else None,
                'is_domain': openstack_project.is_domain,
                self.version_field: self.get_version(timestamp)
            }

            return project_data
        except Exception as e:
            LOG.debug('{} exception when attempting to serialize project'.format(e))

    def delete(self, data, region, timestamp):
        project_id = data['resource_info']
        db_project = Project.objects.filter(project_id=project_id).first()
        if db_project is None:
            LOG.info('Trying to delete project {}: not found in database'.format(project_id))
            return
        if db_project.deleted is True:
            LOG.info(
                'Will not remove the project from db as it was marked as deleted and will be hidden until service '
                'deletion'
            )
            return
        return super(ProjectEventHandler, self).delete(db_project.id, region, timestamp)
