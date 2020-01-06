from __future__ import unicode_literals

from django.urls import reverse
from django.test import TestCase

from fleio.core.tests.factories import ClientFactory, UserFactory


class OpenstackClientsViewSetTest(TestCase):
    def setUp(self):
        self.staff_user = UserFactory.create(id=1, username='testuser', password='staffpass',
                                             email='staff@fleio.com', is_staff=True)
        self.client.login(username=self.staff_user, password='staffpass')

    def test_services_and_projects_does_not_exist(self):
        ClientFactory.create()
        client = ClientFactory.create()

        response = self.client.get(reverse('staff:openstack:clients-openstack-services', args=[client.id]))
        self.api_response = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.api_response['projects']), 0)
        self.assertEqual(len(self.api_response['services']), 0)

    def test_new_service_data(self):
        ClientFactory.create()
        client = ClientFactory.create()
        response = self.client.get(reverse('staff:openstack:clients-new-service-data', args=[client.id]))
        self.api_response = response.json()
        self.assertIn('products', self.api_response)
        self.assertEqual(response.status_code, 200)
