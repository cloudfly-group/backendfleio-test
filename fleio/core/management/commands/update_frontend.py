import sys

from django.core.management.base import BaseCommand

from fleio.core.features import staff_active_features
from fleiostaff.core.frontend_customization.index_manager import IndexManager


class Command(BaseCommand):
    help = 'Update frontend based on settings'

    def handle(self, *args, **options):
        if len(sys.argv) > 1 and sys.argv[1] in ['update_frontend']:
            del sys.argv[1]

        if staff_active_features.is_enabled('demo'):
            self.stdout.write('Frontend cannot be updated in demo mode!')
            return

        self.stdout.write('Updating frontend ...')
        index_manager = IndexManager()
        index_manager.update_frontend()
        self.stdout.write('Fronted updated.')
