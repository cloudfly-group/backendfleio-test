from django.db import models
from django.utils.functional import cached_property

from plugins.domains.custom_fields.contact_custom_field_definition import ContactCustomFieldDefinition
from plugins.domains.models.contact import Contact


class ContactCustomField(models.Model):
    name = models.CharField(max_length=32, db_index=True, null=False, blank=False)
    contact = models.ForeignKey(Contact, related_name='custom_fields', on_delete=models.CASCADE)
    value_type = models.CharField(max_length=16)
    value = models.TextField(max_length=1024)

    class Meta:
        base_manager_name = 'objects'
        unique_together = ('name', 'contact')

    def __str__(self):
        definition_keys = ContactCustomFieldDefinition().definition.keys()
        if self.name in definition_keys:
            return '{} {}'.format(self.contact.name, self.name)
        return '[ Definition missing! ]'

    @cached_property
    def definition(self):
        return ContactCustomFieldDefinition().definition

    @cached_property
    def label(self):
        return self.definition.get(self.name, {}).get('label', '')
