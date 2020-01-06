from fleio.core.custom_fields import custom_fields_definitions
from fleio.core.custom_fields.base import CustomFieldDefinition


class ClientCustomFieldDefinition(CustomFieldDefinition):
    @property
    def original_definition(self):
        return custom_fields_definitions.get_client_definitions()
