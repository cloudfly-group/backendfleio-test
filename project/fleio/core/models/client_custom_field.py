from django.db import models
from django.utils.functional import cached_property

from fleio.core.custom_fields.client_customfield_definition import ClientCustomFieldDefinition


class ClientCustomField(models.Model):
    name = models.CharField(max_length=32, db_index=True, null=False, blank=False)
    client = models.ForeignKey('core.Client', related_name='custom_fields', on_delete=models.CASCADE)
    value_type = models.CharField(max_length=16)
    value = models.TextField(max_length=1024)

    class Meta:
        base_manager_name = 'objects'
        unique_together = ('name', 'client')

    def __str__(self):
        definition_keys = ClientCustomFieldDefinition().definition.keys()
        if self.name in definition_keys:
            return '{} {}'.format(self.client.name, self.name)
        return '[ Definition missing! ]'

    @cached_property
    def definition(self):
        return ClientCustomFieldDefinition().definition

    @cached_property
    def label(self):
        return self.definition.get(self.name, {}).get('label', '')
