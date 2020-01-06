from typing import Dict
from typing import Tuple

from fleio.core.models import Client


class CustomFieldsUtils:
    @staticmethod
    def split_fields_for_client(
            custom_fields: Dict[str, Dict],
            client: Client,
    ) -> Tuple[Dict[str, Dict], Dict[str, Dict]]:
        empty_custom_fields = {}
        filled_custom_fields = {}

        client.cus

        return empty_custom_fields, filled_custom_fields
