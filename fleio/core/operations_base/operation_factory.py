from typing import Optional
import logging

from fleio.core.operations_base.operation_base import OperationBase

LOG = logging.getLogger(__name__)


class OperationsFactory:

    def __init__(self):
        self.registered_classes = {}

    def register_class(self, operation_class: OperationBase):
        self.registered_classes[operation_class.name] = operation_class

    def initialize_class(self, recurring_operation_type: str, db_operation, *args, **kwargs) -> Optional[OperationBase]:
        registered_class = self.registered_classes.get(recurring_operation_type, None)
        if not registered_class:
            LOG.error('Could not load {} recurring operation'.format(recurring_operation_type))
            return None
        return registered_class(db_operation=db_operation, *args, **kwargs)


operations_factory = OperationsFactory()
