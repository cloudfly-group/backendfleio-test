import logging
import sys
from os import environ
from os.path import abspath, dirname

import django

current_path = dirname(abspath(__file__))
fleio_path = dirname(dirname(dirname(current_path)))
sys.path.append(fleio_path)
environ.setdefault("DJANGO_SETTINGS_MODULE", "fleio.settings")
django.setup()

from django.conf import settings  # noqa
from django.utils.translation import ugettext_lazy as _  # noqa

from django.utils.module_loading import import_string  # noqa

from fleio.reports.exceptions import ReportException

LOG = logging.getLogger(__name__)

AVAILABLE_REPORT_TYPES = ('revenue',)

REPORT_TYPE_DETAILS = {
    'revenue': {
        'REPORT_GENERATION_METHOD': 'fleio.reports.revenue_report_generation.generate_revenue_report',
        'feature': settings.STAFF_FEATURES.get('billing.reporting', False),
        'missing_argument_error': 'Please specify month and year in the following format: 03/2019.'
    }
}

if __name__ == '__main__':
    if len(sys.argv) > 1:
        report_type = sys.argv[1]
        report_type_details = REPORT_TYPE_DETAILS.get(report_type, None)
        if report_type_details:
            if len(sys.argv) > 2:
                if report_type_details.get('feature'):
                    generation_argument = sys.argv[2]
                    try:
                        report_generation_method = import_string(report_type_details.get('REPORT_GENERATION_METHOD'))
                    except ImportError:
                        sys.exit(_('Could not find generation method for {}.').format(report_type))
                    else:
                        try:
                            report_generation_method(month_and_year=generation_argument)
                        except ReportException as e:
                            sys.exit(str(e))
                else:
                    sys.exit(_('{} reporting related feature is disabled').format(report_type))
            else:
                sys.exit(report_type_details.get('missing_argument_error'))
        else:
            sys.exit(_('No reporting script found for the reporting type you requested. Available report types are: '
                       '{}').format((','.join(report for report in AVAILABLE_REPORT_TYPES))))
    else:
        sys.exit(_('Please specify the type of report you want to generate when running script. Available report types '
                   'are: {}').format((','.join(report for report in AVAILABLE_REPORT_TYPES))))
