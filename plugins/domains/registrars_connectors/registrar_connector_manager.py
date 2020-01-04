from django.db import IntegrityError

from plugins.domains.custom_fields.configuration import tld_custom_fields

from plugins.domains.models import Contact
from plugins.domains.models import RegistrarConnector

from plugins.domains.registrars_connectors.openprovider_connector import OpenproviderConnector
from plugins.domains.registrars_connectors.registrar_connector_base import RegistrarConnectorBase
from plugins.domains.registrars_connectors.resellerclub_connector import ResellerclubConnector
from plugins.domains.registrars_connectors.rotld_connector import RotldConnector
from plugins.domains.registrars_connectors.todo_registrar_connector import TODORegistrarConnector

from fleio.core.custom_fields import custom_fields_definitions
from fleio.core.models import Client


class RegistrarConnectorInfo:
    def __init__(self, name: str, class_name: classmethod, model: RegistrarConnector, created: bool):
        self.connector_name = name
        self.connector_class = class_name
        self.connector_model = model
        self.created = created
        self.instance = class_name()

    def get_instance(self) -> RegistrarConnectorBase:
        return self.instance


class RegistrarConnectorManager:
    def __init__(self):
        self.connectors_info = {}
        self.connectors_registered = False
        self.register_connectors()
        custom_fields = tld_custom_fields.custom_fields
        for category in custom_fields:
            custom_fields_definitions.add_definitions(
                model=Contact,
                definitions=custom_fields[category],
                category=category,
            )
            custom_fields_definitions.add_definitions(
                model=Client,
                definitions=custom_fields[category],
                category=category,
            )

    def register_connector(self, connector_class):
        connector_name = connector_class.name
        class_name = connector_class.__name__
        try:
            connector_model = RegistrarConnector.objects.create(
                name=connector_name,
                class_name=class_name
            )
            created = True
        except IntegrityError:
            connector_model = RegistrarConnector.objects.get(
                class_name=class_name
            )
            created = False

        connector_info = RegistrarConnectorInfo(
            name=connector_name,
            class_name=connector_class,
            model=connector_model,
            created=created,
        )

        self.connectors_info[connector_name] = connector_info

    def get_connector_instance(self, connector_name: str) -> RegistrarConnectorBase:
        return self.connectors_info[connector_name].get_instance()

    def register_connectors(self):
        if not self.connectors_registered:
            self.register_connector(connector_class=TODORegistrarConnector)
            self.register_connector(connector_class=ResellerclubConnector)
            self.register_connector(connector_class=OpenproviderConnector)
            self.register_connector(connector_class=RotldConnector)
            self.connectors_registered = True


registrar_connector_manager = RegistrarConnectorManager()
