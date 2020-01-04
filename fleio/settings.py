"""
Local settings file

Add any changes to this file.

For more information on this file, see:

https://fleio.com/docs/configuring/settings-file.html
http://www.django-rest-framework.org/api-guide/settings/
https://docs.djangoproject.com/en/2.0/topics/settings/
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

from .base_settings import *  # noqa

# Django secret key
SECRET_KEY = 'wOzKQ)YT8c-lplA)5gkpCCb7^GC!zlz0kG@1RrdhVPu_jFNcYp'

# Salt for signing Single Sign On tokens
SSO_SALT = '5Mr)n0L*wC'

TIME_ZONE = 'Asia/Ho_Chi_Minh'

ADMINS = (
    ('admin admin','vuonglv@inet.vn'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fleio',
        'USER': 'fleio',
        'PASSWORD': 'HEREWETYPEPASSWORD',
        'HOST': 'localhost',
        'PORT': '3306',
        'CONN_MAX_AGE': 500,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_ALL_TABLES'"
        }
    },
}

EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = 'webmaster@localhost'

ALLOWED_HOSTS = ['202.92.6.161']


# You need these settings only if backend and frontend hosts or ports are different

#NEW_MIDDLEWARE = list(MIDDLEWARE)
#NEW_MIDDLEWARE.insert(1, 'corsheaders.middleware.CorsMiddleware')
#NEW_MIDDLEWARE.insert(1, 'fleio.csrf_reseller_pass.CsrfMid')
#MIDDLEWARE = tuple(NEW_MIDDLEWARE)
#RESELLER_DOMAINS = {
#    'resllerdomain1.tld': {
#        'url': 'http://resllerdomain1.tld',
#        'cookie_domain': 'resllerdomain1.tld',
#     },
#    'backend.resllerdomain1.tld': {
#        'url': 'http://resllerdomain1.tld',
#        'cookie_domain': 'resllerdomain1.tld',
#     },
#   'resllerdomain2.tld': {
#       'url': 'http://resllerdomain2.tld',
#        'cookie_domain': 'resllerdomain2.tld',
#     },
#    'backend.resllerdomain2.tld': {
#        'url': 'http://resllerdomain2.tld',
#        'cookie_domain': 'resllerdomain2.tld',
#     },
#}
#CORS_ORIGIN_WHITELIST = (
#   'http://fleio-master.tld',
#)
#CORS_ALLOW_CREDENTIALS = True
#CSRF_TRUSTED_ORIGINS = ['fleio-master.tld']
#for domain in RESELLER_DOMAINS:
#   CORS_ORIGIN_WHITELIST += (RESELLER_DOMAINS[domain]['url'],)
#   CSRF_TRUSTED_ORIGINS.append(domain)
#   ALLOWED_HOSTS.append(domain)


ENABLE_DJANGO_ADMIN = False

# Leave empty to use the default add credit URL of Fleio
# fill in 'client_group_name': 'http://url...' pairs when using an external billing
# when the dictionary has a single entry it will be used regardless of the 'client_group_name'
ADD_CREDIT_URLS = {}

FRONTEND_URL = '202.92.6.161'

# The mapping consists of key-value pairs where the key stands for the client_group and the value will be its
# corresponding frontend URL; each client account will be associated with a group or multiple groups through ClientGroup
# For two frontend urls using the same backend the setting will look like:
# FRONTEND_URL_MAPPING = {'client_group1' : 'http://urlexample1.com/', 'client_group2': 'http://urlexample2.com/'}

# uncomment the following lines to enable the browsable api
# REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
#     REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] + ('rest_framework.renderers.BrowsableAPIRenderer',)
# )

# Proxy settings used for licensing check, only HTTPS is used
# PROXY_SETTINGS = {'https': '10.10.1.11:1080', }

# To enable/disable a payment gateway uncomment the gateway configuration below.
# Settings for each gateway needs to be entered in order for the gateway to function properly.
# Once a gateway is enabled/disabled and the settings file is saved restart your web server and visit the
# gateways page in order for the settings to take effect.

# >>> bank gateway configuration
# bank gateway does not need additional settings and will be enabled by default
# >>> end of bank gateway configuration

'''
# >>> paypal gateway configuration
INSTALLED_APPS += ('fleio.billing.gateways.paypal', )

# paypal gateway settings - fill with the correct values
PAYPAL_SETTINGS = {
    'mode': 'sandbox',  # sandbox or live - set to live for production environment
    'client_id': '',
    'client_secret': '',
    'url_base': 'http://fleio_backend/api/billing/gateway/paypal/'  # replace 'fleio_backend' with correct value
}
# >>> end of paypal gateway configuration
'''

'''
# >>> romcard gateway configuration
INSTALLED_APPS += ('fleio.billing.gateways.romcard', )

# romcard gateway settings - fill with the correct values
ROMCARD_SETTINGS = {
    "merchant_name": "Company",
    "merchant_url": "http://www.site.com",
    "merchant_no": "",
    "terminal": "",
    "recurring_payments_frequency": 28,
    "recurring_payments_expiration_days": 1460,
    "email": "",
    "callback_url":
        "http://fleio_backend/api/billing/gateway/romcard/callback", # replace 'fleio_backend' with correct value
    "encryption_key": "",
    "test_mode": True  # True or False, use False for production environment

}

# >>> end of romcard gateway configuration
'''

'''
# >>> payu gateway configuration
INSTALLED_APPS += ('fleio.billing.gateways.payu', )

# payu gateway settings - fill with the correct values
PAYU_SETTINGS = {
    'orders_url': 'https://secure.snd.payu.com/api/v2_1/orders',
    'authorization_url': 'https://secure.snd.payu.com/pl/standard/user/oauth/authorize',
    'merchant_pos_id': '',
    'client_id': '',
    'client_secret': '',
    'second_key': '',
    'callback_url': 'http://localhost:8000/api/billing/gateway/payu/callback',
}

# >>> end of payu gateway configuration
'''

'''
# >>> stripe gateway configuration
INSTALLED_APPS += ('fleio.billing.gateways.stripe', )

# ATTENTION! if you use recurring payments you will need to add the signing_secret from the webhooks settings page
# Also configure webhooks to send notification ONLY about payment intent events to
# http://your-fleio-address/backend/api/billing/gateway/stripe/callback

# stripe gateway settings - fill with the correct values
STRIPE_SETTINGS = {
    'public_key': '',
    'secret_key': '',
    'signing_secret': '',
    'name': 'Fleio',
    'image_url': 'https://stripe.com/img/documentation/checkout/marketplace.png',
    'locale': 'auto',
    'zipcode': True
}
# >>> end of stripe gateway configuration
'''

'''
# >>> PayU RO gateway configuration
INSTALLED_APPS += ('fleio.billing.gateways.payuro', )

# !! ATTENTION: You need to enable IPN (Instant Payment Notification) notifications from your PayU RO cpanel settings,
# and send notifications only for order authorization (don't send notifications for order confirmations/refunds)

# PayU RO gateway settings - fill with the correct values
PAYURO_SETTINGS = {
    'URL': 'https://sandbox.payu.ro/',
    'MERCHANT_ID': 'xxx',
    'SECRET_KEY': b'xxx',
}
# >>> end of payuro gateway configuration
'''

'''
# Registrars settings
REGISTRARS = {
    'resellerclub': {
        'test': True,
        'auth_userid': '',
        'api_key': ''
    },
    'openprovider': {
        'membership_cost': '0.00',
        'user_id': '',
        'access_hash': ''
    }
}
'''
