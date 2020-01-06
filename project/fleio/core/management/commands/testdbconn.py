from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = ('Test if Fleio can successfully connect to database. '
            'Process exit code is 0 on success and 1 on failure.')
    args = '[silent]'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '-s',
            '--silent',
            action='store_true',
            help='Do not output any message',
        )

    def handle(self, *args, **options):
        db_conn = connections['default']

        try:
            db_conn.cursor()
        except OperationalError:
            if not options['silent']:
                self.stdout.write(self.style.ERROR('Database connection failed'))
            exit(1)
        else:
            if not options['silent']:
                self.stdout.write(self.style.SUCCESS('Successfully connected to database'))
            return 0
