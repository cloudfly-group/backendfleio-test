import logging
from typing import Any
from typing import Dict
from typing import TypeVar

from django.conf import settings

from fleio.core.models.models import Client


LOG = logging.getLogger(__name__)


class CustomFieldDefinitionsManager:
    def __init__(self):
        self.definitions = {}
        self.definitions_by_category = {}
        client_custom_fields = getattr(settings, 'CLIENT_CUSTOM_FIELDS', {})
        self.definitions[Client] = client_custom_fields

    def get_definitions(self, model: TypeVar) -> Dict[str, Dict[str, Any]]:
        definitions = self.definitions.get(model, None)
        if not definitions:
            LOG.info('Custom fields definition not found for type {}'.format(model))
            definitions = {}

        return definitions

    def get_client_definitions(self):
        return self.get_definitions(model=Client)

    def add_definitions(self, model: TypeVar, definitions: Dict[str, Dict[str, Any]], category: str = None):
        model_definitions = self.definitions.setdefault(model, {})
        model_definitions.update(definitions)
        if category:
            model_definitions_categories = self.definitions_by_category.setdefault(model, {})
            model_definitions_categories[category] = definitions

    def remove_definitions(self, model: TypeVar, definitions: Dict[str, Dict[str, Any]], category: str = None):
        """
        This function exists only for testing purposes.
        """
        for field_name in definitions:
            del self.definitions[model][field_name]

        if category:
            model_definitions = self.definitions_by_category.setdefault(model, {})
            del model_definitions[category]


custom_fields_definitions = CustomFieldDefinitionsManager()
