import sys

from django.core.management.base import BaseCommand

from fleio.core.features import staff_active_features
from fleio.core.features import reseller_active_features
from fleio.core.features import active_features


class Command(BaseCommand):
    help = 'Test if a feature is enabled '

    def add_arguments(self, parser):
        parser.add_argument('type', type=str)
        parser.add_argument('feature', type=str)

    def handle(self, *args, **options):
        if options['type'] == 'staff':
            sys.exit(0 if staff_active_features.is_enabled(options['feature']) else 1)

        if options['type'] == 'reseller':
            sys.exit(0 if reseller_active_features.is_enabled(options['feature']) else 1)

        if options['type'] == 'enduser':
            sys.exit(0 if active_features.is_enabled(options['feature']) else 1)

        sys.exit(1)
