from unittest import skip
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from fleio.core.tests.factories import ClientFactory
from fleio.core.utils import random_string
from fleio.openstack.api import identity
from fleio.openstack.models import Project
from fleio.openstack.tests.functional_live_tests import OpenStackInstanceSetup, reverse


# TODO: osbackup is currently disabled. Enable this once osbackup will be enabled again
@skip('osbackup is currently disabled')
class OpenStackCreateBackupScheduleTest(TestCase):
    def setUp(self):
        self.admin_client = identity.IdentityAdminApi()
        self.fleio_client = ClientFactory()
        self.openstack_project = Project.objects.create_project(client=self.fleio_client)
        self.backup_base = OpenStackInstanceSetup(self.client, self.fleio_client, self.admin_client)
        self.backup_name = random_string()

    def test_create_backup(self):
        view = 'backup_schedules'
        response = self.client.post(reverse(view, args=(self.backup_base.instance['uuid'],)),
                                    {'backup_name': self.backup_name,
                                     'backup_type': 'daily',
                                     'rotation': 0,
                                     'run_at': timezone.now() + timedelta(hours=1)})
        self.assertEqual(response.status_code, 201)

    def tearDown(self):
        self.backup_base.nova_client.servers.delete(self.backup_base.instance['uuid'])
        self.admin_client.delete_project(self.backup_base.fleio_client.first_project.project_id)
