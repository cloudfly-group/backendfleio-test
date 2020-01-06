class OperationBase:
    name = 'operation'

    def __init__(self, db_operation):
        self.db_operation = db_operation

    def abort_operation(self):
        """Removes the operation"""
        return self.db_operation.delete()

    def mark_as_completed(self):
        """Marks the operation as completed"""
        self.db_operation.completed = True
        self.db_operation.save()

    def run(self, *args, **kwargs):
        raise NotImplementedError()
