from django.dispatch import Signal


todo_created = Signal(providing_args=['todo'])
todo_deleted = Signal(providing_args=['todo'])
todo_updated = Signal(providing_args=['todo'])
