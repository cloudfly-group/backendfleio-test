import zipfile
from os import remove
from os.path import basename, join, splitext

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = ('Dump test data into a file passed as parameter (optional). '
            'If not specified, testdata.json will be used.')
    args = '[filepath]'

    def add_arguments(self, parser):
        parser.add_argument('--filepath', '-f',
                            action='store',
                            dest='filepath',
                            default=False,
                            help='File path for data dump')
        parser.add_argument('--compress', '-c',
                            action='store_true',
                            default=False,
                            help='Compress if true')

    def handle(self, *args, **options):
        if not options['filepath']:
            testdata_path = join(settings.BASE_DIR, 'testdata.json')
        else:
            testdata_path = options['filepath']
        with open(testdata_path, 'w') as t:
            call_command('dumpdata', use_natural_foreign_keys=True, use_natural_primary_keys=False,
                         indent=4, exclude=['sessions', 'admin.logentry', 'contenttypes', 'auth.permission'], stdout=t)
        if options['compress']:
            with zipfile.ZipFile(splitext(testdata_path)[0] + '.zip', 'w', zipfile.ZIP_DEFLATED) as zip_backup:
                zip_backup.write(testdata_path, basename(testdata_path))
            remove(testdata_path)
