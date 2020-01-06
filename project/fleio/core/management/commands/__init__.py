from django.core.management.base import BaseCommand


class KeepdbCommand(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '-k',
            '--keepdb',
            action='store_true',
            help='Preserves the test DB between runs.',
        )

    def get_test_params(self, standard_params, **options):
        if options['keepdb']:
            return standard_params + ['--keepdb']
        return standard_params
