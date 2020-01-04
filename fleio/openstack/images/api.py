import copy
import json
import tempfile
import logging
from glanceclient import exc as glance_exceptions
from django.conf import settings

from fleio.openstack.api.glance import glance_client
from fleio.openstack.images.tasks import import_image_from_url
from fleio.openstack.images.tasks import import_image_from_file

LOG = logging.getLogger(__name__)


def get_metadata_catalog(api_session):
    gc = glance_client(api_session)

    catalog = [
        namespace.__original__
        for namespace in gc.metadefs_namespace.list(filters={'resource_types': 'OS::Glance::Image'})
    ]

    for namespace in catalog:
        ns_properties = []
        ns_objects = []

        for ns_property in gc.metadefs_property.list(namespace=namespace['namespace']):
            ns_properties.append(ns_property)

        if ns_properties:
            namespace.update(properties=ns_properties)

        for ns_object in gc.metadefs_object.list(namespace=namespace['namespace']):
            ns_objects.append(ns_object)

        if ns_objects:
            namespace.update(objects=ns_objects)

    return catalog


class Images:
    def __init__(self, api_session):
        """
        :type api_session: keystoneauth1.session.Session
        """
        self.api_session = api_session

    def get(self, image):
        """
        :type image: fleio.openstack.models.Image
        :rtype: Image
        """
        return Image(image, api_session=self.api_session)

    @staticmethod
    def unset_properties_if_same_value(gc, image, properties, remove_props):
        image.properties.pop('os_distro', None)
        image.properties.pop('os_version', None)
        image.properties.pop('architecture', None)
        for prop in image.properties:
            for curr_prop in properties:
                if image.properties[prop] == properties[curr_prop] and prop != curr_prop:
                    gc.images.update(image.id, remove_props=remove_props)
                    return

    def download(self, image):
        gc = glance_client(self.api_session, region_name=image.region.id)
        return gc.images.data(image_id=image.id)

    def update(self, image, **fields):
        gc = glance_client(self.api_session, region_name=image.region.id)
        fields_copy = copy.deepcopy(fields)
        properties = fields_copy.pop('properties', None)
        remove_props = []

        non_removable_properties = ('owner', 'name', 'min_disk', 'min_ram', 'container_format', 'disk_format',
                                    'visibility', 'protected', 'region')
        for prop_name, prop_value in iter(fields.items()):
            if prop_name not in non_removable_properties:
                if prop_value is None or prop_value == '':
                    fields_copy.pop(prop_name)
                    remove_props.append(prop_name)

        props = {}
        if properties:
            if isinstance(properties, str):
                try:
                    properties = json.loads(properties)
                except json.decoder.JSONDecodeError:
                    properties = {}
            properties.pop('os_distro', None)
            properties.pop('os_version', None)
            properties.pop('hypervisor_type', None)
            properties.pop('architecture', None)
            props = copy.deepcopy(properties)
            for name, value in iter(properties.items()):
                if value is None or value == '':
                    remove_props.append(name)
                    props.pop(name)

        # can't set and remove a property with the same value (bug in client), so first we must
        # unset the variable, then set the new key
        self.unset_properties_if_same_value(gc, image, properties, remove_props)

        return gc.images.update(image.id, remove_props=remove_props, **fields_copy, **props)

    def deactivate(self, image):
        gc = glance_client(self.api_session, region_name=image.region.id)
        return gc.images.deactivate(image_id=image.id)

    def reactivate(self, image):
        gc = glance_client(self.api_session, region_name=image.region.id)
        return gc.images.reactivate(image_id=image.id)

    def create(self, owner, name, min_disk, min_ram, container_format='bare', disk_format='qcow2',
               visibility='private', protected=False, architecture=None, os_distro=None, os_version=None, region=None,
               hypervisor_type=None, file=None, url=None, source=None, properties=None):

        optional_data = {}
        if architecture:
            optional_data['architecture'] = architecture
        if os_distro:
            optional_data['os_distro'] = os_distro
        if hypervisor_type:
            optional_data['hypervisor_type'] = hypervisor_type
        if os_version:
            optional_data['os_version'] = os_version

        if properties:
            optional_data.update(properties)

        if region is not None:
            region_name = region.id
        else:
            region_name = None

        gc = glance_client(api_session=self.api_session, region_name=region_name)
        # NOTE(tomo): First create the image, upload needs to happen after
        openstack_image = gc.images.create(name=name, owner=owner, container_format=container_format,
                                           disk_format=disk_format, min_disk=min_disk, min_ram=min_ram,
                                           visibility=visibility, protected=protected, **optional_data)

        if source == 'file' and file:
            # save the uploaded file
            image_temp_dir = getattr(settings, 'OPENSTACK_IMAGE_TEMP_DIR', None)
            with tempfile.NamedTemporaryFile(prefix=openstack_image.id,
                                             dir=image_temp_dir,
                                             delete=False) as temp_image_file:
                for chunk in file.chunks():
                    if chunk:
                        temp_image_file.write(chunk)
                temp_image_file.close()
            import_image_from_file.delay(openstack_image.id,
                                         region_name=region_name,
                                         file_path=temp_image_file.name)
        elif source == 'url':
            import_image_from_url.delay(openstack_image.id, url=url, region_name=region_name)
        return openstack_image


class Image:
    def __init__(self, db_image, api_session=None):
        """
        :type db_image: fleio.openstack.models.Image
        """
        self.db_image = db_image
        self.api_session = api_session

    @property
    def glance_api(self):
        """
        :rtype: glanceclient.v2.client.Client
        """
        assert self.api_session is not None, 'Unable to use glance_api without an api_session!'

        return glance_client(api_session=self.api_session, region_name=self.db_image.region.id)

    def delete(self):
        """Delete the image from Glance."""
        try:
            self.glance_api.images.delete(image_id=self.db_image.id)
        except glance_exceptions.NotFound:
            self.db_image.delete()

    def deactivate(self):
        return self.glance_api.images.deactivate(image_id=self.db_image.id)

    def reactivate(self):
        return self.glance_api.images.reactivate(image_id=self.db_image.id)

    def create_member(self, member_project_id):
        return self.glance_api.image_members.create(image_id=self.db_image.id, member_id=member_project_id)

    def update_member(self, member_project_id, member_status):
        return self.glance_api.image_members.update(
            image_id=self.db_image.id, member_id=member_project_id, member_status=member_status
        )

    def delete_member(self, member_project_id):
        return self.glance_api.image_members.delete(image_id=self.db_image.id, member_id=member_project_id)

    def set_visibility(self, visibility):
        """Set the visibility attribute of an image"""
        return self.glance_api.images.update(image_id=self.db_image.id, visibility=visibility)
