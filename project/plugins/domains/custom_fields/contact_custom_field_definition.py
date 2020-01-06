from fleio.core.custom_fields import custom_fields_definitions
from fleio.core.custom_fields.base import CustomFieldDefinition


from plugins.domains.models.contact import Contact


class ContactCustomFieldDefinition(CustomFieldDefinition):
    @property
    def original_definition(self):
        return custom_fields_definitions.get_definitions(model=Contact)
