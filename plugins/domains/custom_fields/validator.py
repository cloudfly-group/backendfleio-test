from typing import List
from typing import Tuple

from fleio.core.models.client_custom_field import ClientCustomField

from plugins.domains.custom_fields.configuration import tld_custom_fields
from plugins.domains.models import ContactCustomField
from plugins.domains.utils.domain import DomainUtils


class CustomFieldsValidator:
    # TODO: remove duplicate code between these two functions
    @staticmethod
    def client_has_missing_fields_for_domain(client_id: int, domain_name: str) -> Tuple[bool, List[str]]:
        tld = DomainUtils.get_tld(domain_name=domain_name)
        custom_fields = tld_custom_fields.get_definitions_for_tld(
            tld_name=tld.name,
        )

        custom_field_names = [
            name for name, field_definition in custom_fields.items() if field_definition.get('required_for_domain')
        ]
        fields_with_values_in_db = ClientCustomField.objects.filter(
            client_id=client_id,
        ).exclude(
            value__isnull=True,
        ).exclude(
            value__exact=''
        ).values_list('name', flat=True)

        missing_fields = [
            field_name for field_name in custom_field_names if field_name not in fields_with_values_in_db
        ]

        missing_field_labels = [custom_fields[field_name]['label'] for field_name in missing_fields]

        return len(missing_field_labels) > 0, missing_field_labels

    @staticmethod
    def contact_has_missing_fields_for_domain(contact_id: int, domain_name: str) -> Tuple[bool, List[str]]:
        tld = DomainUtils.get_tld(domain_name=domain_name)
        custom_fields = tld_custom_fields.get_definitions_for_tld(
            tld_name=tld.name,
        )

        custom_field_names = [name for name in custom_fields]
        fields_with_values_in_db = ContactCustomField.objects.filter(
            contact_id=contact_id,
        ).exclude(
            value__isnull=True,
        ).exclude(
            value__exact=''
        ).values_list('name', flat=True)

        missing_fields = [
            field_name for field_name in custom_field_names if field_name not in fields_with_values_in_db
        ]

        missing_field_labels = [custom_fields[field_name]['label'] for field_name in missing_fields]

        return len(missing_field_labels) > 0, missing_field_labels
