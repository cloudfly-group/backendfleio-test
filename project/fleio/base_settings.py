"""
Base settings file.

Do not modify this file as it will ve overwritten on updates.
Edit settings.py instead.
"""

import bleach.sanitizer
import logging
import os
import sys
import crypt
import urllib3
from cryptography.hazmat.primitives import serialization as crypto_serialization


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_STAFF_DIR = '/var/webapps/fleio/frontend/site/staff'
FRONTEND_SITE_DIR = '/var/webapps/fleio/frontend/site'
FLEIO_TEMP_DIR = '/var/fleio/tmp'
ATTACHMENTS_DIR = '/var/fleio/attachments'
FRONTEND_UPDATES_DIR = '/var/fleio/frontend'
FRONTEND_UPDATES_STAFF_DIR = '/var/fleio/frontend/staff'
FRONTEND_UPDATES_SITE_DIR = '/var/fleio/frontend/site'
FREE_DISK_SPACE_LIMIT = 52428800  # 50MB
TASK_LOG_DIR = '/var/log/fleio/tasklog'


class InfoFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno in (logging.INFO, logging.DEBUG, logging.NOTSET)


def _(s):
    # work around for using i18n in settings
    return s


USE_TZ = True

MIDDLEWARE = (
    'fleio.conf.middleware.ConfigurationErrorMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'fleiostaff.core.middleware.check_license.CheckLicenseMiddleware',
    'fleiostaff.core.middleware.impersonate_user.ImpersonateUserMiddleware',
    'fleio.core.middleware.check_clients.CheckClientsMiddleware',
    'fleio.core.middleware.check_emails.CheckUserEmailMiddleware',
    'fleio.core.middleware.check_tos.CheckTOSMiddleware',
    'fleio.core.middleware.check_sfa.CheckSFAMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

ROOT_URLCONF = 'fleio.urls'
PLUGIN_URLS_BASE_PATH = 'plugins/'

WSGI_APPLICATION = 'fleio.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django_extensions',
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    'fleio.conf',
    'fleio.core',
    'fleio.activitylog',
    'fleio.pkm',
    'fleio.openstack',
    'fleio.reseller',
    'fleio.osbackup',
    'fleio.notifications',
    'fleio.osbilling',
    'fleio.billing',
    'fleio.billing.gateways.bank',
    'fleio.tasklog',
    'fleio.servers',
    'fleio.reports',
    'plugins.todo',
    'plugins.tickets',
    'plugins.cpanel',
    'plugins.cpanelserver',
    'plugins.domains',
    'plugins.hypanel',
    'plugins.google_authenticator',
    'plugins.sms_authenticator',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache'
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'detailed': {
            'format': '%(levelname)s %(asctime)s %(module)s %(funcName)s %(message)s'
        },
        'simple': {
            'format': '##### %(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
        'info_filter': {
            '()': 'fleio.base_settings.InfoFilter'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'detailed'
        },
        'stdout': {
            'filters': ['require_debug_true', 'info_filter'],
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'detailed'
        },
        'stderr': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'stream': sys.stderr,
            'formatter': 'detailed'
        }
    },
    'loggers': {
        '': {
            'handlers': ['stdout', 'stderr'],
            'propagate': True,
            'level': 'ERROR'
        },
        'cron': {
            'handlers': ['stdout', 'stderr'],
            'propagate': False,
            'level': 'ERROR',
        }
    }
}

LOGGING['loggers']['cron']['level'] = os.environ.get('CRON_LOG_LEVEL', 'ERROR')

REST_FRAMEWORK = {
    'DEFAULT_MODEL_SERIALIZER_CLASS': 'rest_framework.serializers.HyperlinkedModelSerializer',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'fleio.core.drf.FakeFormBasedAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'PAGE_SIZE': 20,
    'DEFAULT_PAGINATION_CLASS': 'fleio.core.drf.FleioPaginationSerializer',
    'NUM_PROXIES': 0,
    'DEFAULT_THROTTLE_RATES': {
        'login': '60/hour',
        'django_admin': '60/hour',
        'signup': '2/day',
        'confirm_email': '100/day',
        'resend_email_verification': '100/day',
        'password_reset': '10/hour',
        'gateway_callback': '1000/hour',
        'anonymous_sms_authenticator': '60/hour',
        'sms_sending': '15/hour',
    },
    'DEFAULT_VERSIONING_CLASS': 'fleio.core.drf.FleioVersioning',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        # uncomment the following line to enable the browsable api
        # 'rest_framework.renderers.BrowsableAPIRenderer',
        'fleio.core.drf.FleioJsonRenderer',
    ),
    'EXCEPTION_HANDLER': 'fleio.core.drf_exception_handler.drf_exception_handler'
}

GRANT_ALL_PERMISSIONS_IMPLICITLY = True

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.AllowAllUsersModelBackend', )
APPEND_SLASH = True

URL_PREFIX = 'backend/'  # if not empty must end with a slash '/'

ENABLE_DJANGO_ADMIN = False

DJANGO_ADMIN_URL_PREFIX = 'admin/'

STATIC_URL = '/static/'
SITE_ID = 1
SSO_MAX_AGE = 5  # SSO signature timeout in seconds

BIND_SESSION_IP_STAFF_USER = False
BIND_SESSION_IP_END_USER = False

LICENSING_SERVER_URL = 'https://licensing.fleio.com/'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

PASSWORD_RESET_TIMEOUT_DAYS = 1

FLEIO_BACKEND_VERSION = '2019.12.0'
FLEIO_BACKEND_BUILD= '71868fb'
FLEIO_LATEST_FRONTEND_VERSION = '2019.12.0'
FLEIO_LATEST_FRONTEND_BUILD= '71868fb'

AUTH_USER_MODEL = 'core.AppUser'

CLIENT_CUSTOM_FIELDS = {}

LOCALE_PATHS = [
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'locale'),
]

LANGUAGES = (
    ('en', 'English'),
    ('ro', 'Română'),
)

DEFAULT_USER_LANGUAGE = 'en'

# if you're going to modify this, make sure you have all current notification templates translated in the new language
DEFAULT_NOTIFICATION_TEMPLATE_LANGUAGE_CODE = 'en'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Add null handler for logging pycountry.db to remove warnings at running django commands
logging.getLogger('pycountry.db').addHandler(logging.NullHandler())

# European Union Countries for VAT ID validation
EU_COUNTRIES = ['AD', 'AL', 'AT', 'BE', 'BG', 'BY', 'CZ', 'DE', 'DK', 'EE', 'FI', 'FR', 'GR', 'HU', 'IE', 'IS',
                'IT', 'LI', 'LT', 'LU', 'LV', 'MK', 'MT', 'NL', 'NO', 'PL', 'PT', 'RO', 'RU', 'SE', 'SI', 'SK',
                'SM', 'UA', 'VA', 'BA', 'HR', 'MD', 'MC', 'ME', 'RS', 'ES', 'CH', 'GB']

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0/'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_ENABLE_UTC = True
CELERY_IGNORE_RESULT = True
CELERY_TASK_SOFT_TIME_LIMIT = 1200
CELERY_TASK_TIME_LIMIT = 1500

TASK_RETRIES = 5  # how many times to retry to run a task if it fails?


def get_task_retry_delay(retry_no):  # no
    """
    :param retry_no: the number of times the task has been retried
    :return: the number of seconds to wait before trying to rerun a failing task
    """
    return 2 ** retry_no


FLEIO_RANDOM_ID = {
    'default': {'MIN': 1000,
                'MAX': 999999,
                'GROWTH_FACTOR': 10,
                'GROW_AFTER_COLLISIONS': 5}
}

# Feature declaration uses two values to define feature accessibility.
# True - The feature requires authentication and it is enabled.
# False - The feature does not require authentication and it is enabled.
# sub-features can be identified as '<main-feature>.<sub-feature>', i.e 'openstack.instances.snapshots'
FEATURES = {
    'demo': False,
    'enduser': True,
    'enduser.allow_changing_password': True,
    'billing': True,
    'billing.addcredit': True,
    'billing.history': True,
    'billing.invoices': True,
    'billing.order': True,
    'billing.pdf': True,
    'billing.services': True,
    'billing.recurring_payments': False,
    'clients&users.clients': True,
    'clients&users.signup': True,
    'clients&users.users': True,
    'clients&users.userprofile': True,
    'clients&users.second_factor_auth': True,
    'clients&users.second_factor_auth.google_authenticator': True,
    'clients&users.second_factor_auth.sms_authenticator': True,
    'dashboard': True,
    'notifications': True,
    'openstack': True,
    'openstack.apiusers': True,
    'openstack.cleanup': True,
    'openstack.cleanup.images': True,
    'openstack.cleanup.images.showdate': True,
    'openstack.coe.clusters': True,
    'openstack.coe.cluster_templates': True,
    'openstack.dns.ptr': True,
    'openstack.dns.zones': True,
    'openstack.flavors': True,
    'openstack.floatingips': True,
    'openstack.images': True,
    'openstack.images.download': True,
    'openstack.images.file_uploads': True,
    'openstack.images.updatecreate': True,
    'openstack.images.showcommunity': True,
    'openstack.images.showshared': True,
    'openstack.instances': True,
    'openstack.instances.allow_changing_password': True,
    'openstack.instances.resize.allow_resize_to_less_disk_space': True,
    'openstack.instances.snapshots': True,
    'openstack.instances.snapshots.pricing': True,
    'openstack.instances.traffic': True,
    'openstack.instances.networking.edit': True,
    'openstack.networks': True,
    'openstack.networks.display_external_networks': True,
    'openstack.networks.display_shared_networks': True,
    'openstack.ports': True,
    'openstack.projects': True,
    'openstack.routers': True,
    'openstack.securitygroups': True,
    'openstack.sshkeys': True,
    'openstack.subnetpools': True,
    'openstack.volumes': True,
    'openstack.volumes.backups': True,
    'openstack.volumes.snapshots': True,
    'openstack.volumes.boot': True,
    'openstack.osbackup': True,
    'openstack.osbackup.schedules': True,
    'plugins': True,
    'plugins.todo': True,
    'plugins.tickets': True,
    'plugins.cpanel': True,
    'plugins.cpanelserver': True,
    'plugins.domains': True,
    'plugins.hypanel': False,
}


# dependencies between features in the following format
# feature name : list of required features
FEATURES_DEPENDENCIES = {
    'openstack.instances.networking.edit': ['openstack.ports'],
}

RESELLER_FEATURES = {
    'demo': False,
    'reseller': True,

    'billing': True,
    'billing.transactions': True,
    'billing.journal': True,
    'billing.invoices': True,
    'billing.orders': True,
    'billing.products': True,
    'billing.pdf': True,
    'billing.services': True,
    'billing.history': True,
    'clients&users.clients': True,
    'clients&users.clientgroups': True,
    'clients&users.userprofile': True,
    'clients&users.users': True,
    'clients&users.usergroups': True,
    'clients&users.second_factor_auth': True,
    'clients&users.second_factor_auth.google_authenticator': True,
    'clients&users.second_factor_auth.sms_authenticator': True,
    'notifications': True,
    'notifications.send': False,
    'openstack': True,
    'openstack.apiusers': True,
    'openstack.cleanup': True,
    'openstack.cleanup.images': True,
    'openstack.cleanup.images.showdate': True,
    'openstack.coe.clusters': True,
    'openstack.coe.cluster_templates': True,
    'openstack.dns.ptr': True,
    'openstack.dns.zones': True,
    'openstack.flavors': True,
    'openstack.floatingips': True,
    'openstack.images': True,
    'openstack.images.download': True,
    'openstack.images.file_uploads': True,
    'openstack.images.shareoncreate': True,
    'openstack.images.showcommunity': True,
    'openstack.images.showshared': True,
    'openstack.instances': True,
    'openstack.instances.allow_changing_password': True,
    'openstack.instances.snapshots': True,
    'openstack.instances.traffic': True,
    'openstack.networks': True,
    'openstack.ports': True,
    'openstack.projects': True,
    'openstack.routers': True,
    'openstack.securitygroups': True,
    'openstack.sshkeys': True,
    'openstack.subnetpools': True,
    'openstack.subnets': True,
    'openstack.volumes': True,
    'openstack.volumes.backups': True,
    'openstack.volumes.snapshots': True,
    'openstack.volumes.boot': True,
    'openstack.osbackup': True,
    'openstack.osbackup.schedules': True,
    'openstack.plans': True,
    'plugins': True,
    'plugins.cpanel': True,
    'plugins.cpanelserver': True,
    'plugins.domains': True,
    'plugins.todo': True,
    'plugins.tickets': True,
    'plugins.hypanel': False,
    'settings.configurations': True,
    'servers': True,
}

# dependencies between features in the following format
# feature name : list of required features
RESELLER_FEATURES_DEPENDENCIES = {
}

STAFF_FEATURES = {
    'demo': False,
    'staff': True,

    'billing': True,
    'billing.gateways': True,
    'billing.journal': True,
    'billing.invoices': True,
    'billing.orders': True,
    'billing.products': True,
    'billing.pdf': True,
    'billing.services': True,
    'billing.taxrules': True,
    'billing.transactions': True,
    'billing.reporting': True,
    'billing.reseller': False,
    'clients&users.clients': True,
    'clients&users.clientgroups': True,
    'clients&users.userprofile': True,
    'clients&users.users': True,
    'clients&users.usergroups': True,
    'clients&users.second_factor_auth': True,
    'clients&users.second_factor_auth.google_authenticator': True,
    'clients&users.second_factor_auth.sms_authenticator': True,
    'dashboard': True,
    'app-status': True,
    'notifications': True,
    'notifications.send': False,
    'openstack': True,
    'openstack.apiusers': True,
    'openstack.cleanup': True,
    'openstack.cleanup.images': True,
    'openstack.cleanup.images.showdate': True,
    'openstack.coe.clusters': True,
    'openstack.coe.cluster_templates': True,
    'openstack.dns.ptr': True,
    'openstack.dns.zones': True,
    'openstack.flavors': True,
    'openstack.floatingips': True,
    'openstack.images': True,
    'openstack.images.download': True,
    'openstack.images.file_uploads': True,
    'openstack.images.shareoncreate': True,
    'openstack.images.showcommunity': True,
    'openstack.images.showshared': True,
    'openstack.instances': True,
    'openstack.instances.allow_changing_password': True,
    'openstack.instances.snapshots': True,
    'openstack.instances.traffic': True,
    'openstack.networks': True,
    'openstack.ports': True,
    'openstack.projects': True,
    'openstack.routers': True,
    'openstack.securitygroups': True,
    'openstack.sshkeys': True,
    'openstack.subnetpools': True,
    'openstack.subnets': True,
    'openstack.volumes': True,
    'openstack.volumes.backups': True,
    'openstack.volumes.snapshots': True,
    'openstack.volumes.boot': True,
    'openstack.osbackup': True,
    'openstack.osbackup.schedules': True,
    'openstack.settings': True,
    'openstack.plans': True,
    'plugins': True,
    'plugins.cpanel': True,
    'plugins.cpanelserver': True,
    'plugins.domains': True,
    'plugins.todo': True,
    'plugins.tickets': True,
    'plugins.hypanel': False,
    'settings': True,
    'settings.general': True,
    'settings.configurations': True,
    'settings.authorization': True,
    'settings.notifications.templates': True,
    'utils': True,
    'utils.activitylog': True,
    'utils.tasklog': True,
    'utils.reports': True,
    'servers': True,
}

# dependencies between features in the following format
# feature name : list of required features
STAFF_FEATURES_DEPENDENCIES = {
}


ADD_CREDIT_URLS = {}
FRONTEND_URL = ''
STAFF_FRONTEND_URL_ENDPOINT = 'staff/'
RESELLER_FRONTEND_URL_ENDPOINT = 'reseller/'

# Used for multiple frontend instances using the same backend
FRONTEND_URL_MAPPING = {}

FLEIO_API_VERSIONS = {
    'compute': {
        'min_version': '2.25',
        'max_version': '2.72'
    },
    'identity': {
        'min_version': '3.0',
        'max_version': '3.12'
    },
    'volume': {
        'min_version': '3.18',
        'max_version': '3.59'
    },
    'volumev2': {
        'min_version': '2.0',
        'max_version': '2.0'
    },
    'volumev3': {
        'min_version': '3.0',
        'max_version': '3.59'
    },
    'image': {
        'min_version': '2.0',
        'max_version': '2.7'
    },
    'metric': {
        'min_version': '1.0',
        'max_version': '1.0'
    },
    'network': {
        'min_version': '2.0',
        'max_version': '2.0'
    },
    'dns': {
        'min_version': '2.0',
        'max_version': '2.0'
    },
    'container-infra': {
        'min_version': '1.0',
        'max_version': '1.7',
    }
}

OPENSTACK_NETWORK_PROVIDER_TYPES = ['local', 'flat', 'vlan', 'vxlan', 'gre', 'geneve']
OPENSTACK_DEFAULT_VOLUME_SERVICE_TYPE = 'volumev3'
OPENSTACK_CREATE_FROM_ISO_IMAGE_TYPE = 'raw'
OPENSTACK_CREATE_FROM_ISO_PROPERTY_PREFIXES = ['hw_']
OPENSTACK_EVENT_NOTIFICATIONS_LOGGING_KEYWORDS = []
# Will log event notification to /var/log/fleio/os_event_notifications.txt that contain or ar the same as the keywords
# defined here. Example: OPENSTACK_EVENT_NOTIFICATIONS_LOGGING_KEYWORDS = ['instance', 'snapshot.update.start']

PROXY_SETTINGS = None

# Name of the security group that is automatically created when the end-user creates the first instance
SECURITY_GROUP_NAME = 'fleio'
# Description of the same automatically created security group
SECURITY_GROUP_DESCRIPTION = 'fleio'

# OSBILLING Settings
OSBILLING_TIME_ROUNDING = 'ROUND_UP'
OSBILLING_INTER_TIME_ROUNDING_PREC = '0.000000001'
OSBILLING_TIME_ROUNDING_PREC = '1.'
OSBILLING_INTER_PRICE_ROUNDING = 'ROUND_HALF_UP'
OSBILLING_INTER_PRICE_PREC = '0.000000001'
OSBILLING_INTER_PRICE_DISPLAY_PREC = '0.0001'
OSBILLING_PRICE_ROUNDING = 'ROUND_HALF_UP'
OSBILLING_PRICE_PREC = '0.01'
OSBILLING_NEGATIVE_PRICE_ALWAYS_ZERO = True  # Negative pricing for resources will always be rounded up to zero

INSTANCE_SNAPSHOT_PRICE_TIME_UNIT = 'h'
INSTANCE_SNAPSHOT_PRICE_ATTRIBUTE_UNIT = 'g'
INSTANCE_SNAPSHOT_PRICE_PREC = '0.01'

# bleach settings
bleach.sanitizer.ALLOWED_TAGS += [
    'img',
    'p',
    'span',
    'div',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'br',
    'ol',
    'ul',
    'li',
    'blockquote',
    'pre',
]

bleach.sanitizer.ALLOWED_ATTRIBUTES.update(
    {
        'img': [
            'alt',
            'src',
            'width',
            'height',
        ],
        'p': [
            'style'
        ],
        'span': [
            'style'
        ],
        'h1': [
            'style'
        ],
        'h2': [
            'style'
        ]
    }
)

bleach.sanitizer.ALLOWED_STYLES += [
    'text-align',
    'padding-left',
    'text-decoration'
]

MAX_TICKET_ATTACHMENT_SIZE = 26214400  # 25MB
MAX_EMAIL_ATTACHMENT_SIZE = 10 * 1024 * 1024  # 10MB

TICKET_ID_DEFAULT_FORMAT = '%n%n%n%n%n%n'
TICKET_ID_MIN_RANDOM_CHARS = 6

UPDATE_RELATIVE_PRICES_BEFORE_PROCESSING_CLIENTS = False

REGISTRARS = {}

"""
Available exchange rate connectors:
ECBConnector (European Central Bank connector, relative to EUR currency),
BNRConnector (Romanian National Bank connector, relative to RON currency)
e.g.: DEFAULT_EXCHANGE_RATE_CONNECTOR = 'ECBConnector'
"""
DEFAULT_EXCHANGE_RATE_CONNECTOR = None
AUTO_UPDATE_EXCHANGE_RATES = False

ROTLD_PRICES = {
    'min_years': None,
    'max_years': None,
    'register_price': None,
    'transfer_price': None,
    'renew_price': None,
    'promo_price': None,
}

INVOICE_CUSTOMER_DETAILS_GETTER = 'fleio.billing.utils.get_customer_invoice_details'

# LXC console settings
ENABLE_LXC_CONSOLE = False
LXC_CONSOLE_PROXY_PORT = 8999
LXC_CONSOLE_PROXY_SERVICE_TYPE = None


# CUSTOM MENU OPTIONS DEFINITION
CUSTOM_MENU_CATEGORIES_ENDUSER = {}
CUSTOM_MENU_OPTIONS_ENDUSER = []
CUSTOM_MENU_CATEGORIES_STAFF = {}
CUSTOM_MENU_OPTIONS_STAFF = []

EMAIL_VERIFICATION_TIMEOUT_DAYS = 1

"""SEND_OPENSTACK_ERRORS_ON_EVENTS: usage example below
(note that you can use '*' attribute to catch all error notifications)"""
# notifications are those received from openstack
# besides these, you can use other notification names used in fleio: fleio_instance_create
SEND_OPENSTACK_ERRORS_ON_EVENTS = {
    # 'compute_task.build_instances': {
    #     'error_receivers': {
    #         'staff_users': False,
    #         'custom_emails': [],
    #     },
    #     'full_json': False,
    # }
}

# PTR_DEFAULT_FORMAT will be set on ip allocation/de-allocation
# use None value for PTR_DEFAULT_FORMAT so it won't change ptr record on above actions (same for IPV6)
# if you want to change ptr record on above actions,
# use the following string format: '{dashed_ip}.static.yourclouddomain.com'
# make sure you also set the INVERSE_ADDRESS_ZONE_DEFAULT_EMAIL setting if you wish to use the default PTR feature
PTR_DEFAULT_FORMAT = None
PTR_DEFAULT_FORMAT_IPV6 = None
INVERSE_ADDRESS_ZONE_DEFAULT_EMAIL = 'hostmaster@yourclouddomain.com'

REPORTING_DEFAULT_LOCATION = 'Default'
REVENUE_REPORTING_TIMEZONE = None
# for REVENUE_REPORTING_TIMEZONE use a string stating the timezone, eg: 'Europe/Bucharest'

UPDATED_LOCK_FILE = '/var/fleio/updated_lock.pid'
PROCESS_CLIENT_CRON_LOCK_FILE = '/var/fleio/process_client_cron_lock_file.pid'

# settings for saving received emails that pass through the incoming_mail script from tickets plugin
LOG_EMAILS_RELATED_TO_TICKETS = False  # enable/disable feature
LOGGED_TICKET_EMAILS_LOCATION = '/var/fleio/ticket_emails'  # location of saved emails
MAX_LOGGED_TICKET_EMAIL_SIZE = 104857600  # max size of an email that is logged (defaults to 100MB)

OS_HYPERVISOR_TYPES = ('hyperv', 'ironic', 'lxc', 'qemu', 'uml', 'vmware', 'xen', 'kvm', 'lxd',)

# Move to settings.py file if you want to customize second factor authentication settings
REMEMBER_SECOND_FACTOR_AUTH_DAYS = 60  # - number of days that a logged in user won't be required to submit again
# the second factor authentication form after he opted for remembering the browser
ALLOW_CHANGING_SFA_AFTER_LOGIN_MINUTES = 5  # - minutes after user logs in that he is allowed to enter sfa settings
# without re-entering his password

GOOGLE_AUTHENTICATOR_SETTINGS = {
    # 'issuer_name': 'Fleio app'
}
SMS_AUTHENTICATOR_SETTINGS = {
    'provider': 'amazon_sms_provider',
    'message': 'Hello, your Fleio verification code is {}',
    'subject': None,
}

AMAZON_SMS_PROVIDER_SETTINGS = {
    # 'aws_access_key_id': '',
    # 'aws_secret_access_key': '',
    # 'region_name': '',
    # 'verify': False,
}

STAFF_INSTANCE_ADDITIONAL_CLOUD_INIT_USERDATA = None  # userdata ran on staff launched instances

ENDUSER_INSTANCE_ADDITIONAL_CLOUD_INIT_USERDATA = None  # userdata ran on end-user launched instances

INSTANCE_REBUILD_ADDITIONAL_USER_DATA = None  # userdata ran when a server is rebuilt

'''
Use the template defined below in above cloud-init additional userdata settings (redefine them in settings.py)
to automatically install qemu guest agent on instances in order for OpenStack password changing feature to work
"""#cloud-config
packages:
  - qemu-guest-agent
"""
'''


INSTANCE_CLOUD_INIT_ROOT_PASSWORD_SET = """#cloud-config
ssh_pwauth: True 
disable_root: false 
chpasswd:
  list: |
    root:{root_password}
  expire: False
"""  # noqa

INSTANCE_CLOUD_INIT_SSH_KEYS_SET = """#cloud-config
users:
  - name: {user}
    ssh-authorized-keys:\n"""  # noqa

INSTANCE_CLOUD_INIT_NEW_USER_AND_PASSWORD_SET = """#cloud-config
ssh_pwauth: True 
disable_root: false 
users:
  - default
  - name: {new_user_name}
    sudo: ALL=(ALL) NOPASSWD:ALL
    lock_passwd: false

chpasswd:
  list: |
    {new_user_name}:{new_user_password}
  expire: False
"""  # noqa

INSTANCE_PASSWORD_HASH_METHOD = crypt.METHOD_SHA512

# instance traffic to display when collecting trafic data. Available options are 'public' and 'all'
INSTANCE_TRAFFIC_DISPLAY = 'all'
TRAFIC_DATA_GRANULARITY = 300

STATE_REQUIRED_FOR_COUNTRY = {
    'FR': False,
}

RECURRENT_PAYMENTS_TERMS_AND_CO_DEFAULT = (
    '<span>Save my card for automatic payments. I agree with the <a class="md-primary" target="_blank" '
    'ng-click="$ctrl.clickedConditions()" href="http://fleio.com"> terms & conditions.</a></span>'
)

SSH_PRIVATE_KEY_FORMAT = crypto_serialization.PrivateFormat.TraditionalOpenSSL
# you can also use PrivateFormat.PKCS8

# will not allow users to choose to upload a file that is not in this list. Leave empty to allow any format
OS_IMAGE_UPLOAD_FORMATS = []
# example usage: OS_IMAGE_UPLOADS_FORMATS = ['img', 'iso']
