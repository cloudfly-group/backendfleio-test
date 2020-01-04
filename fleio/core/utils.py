import json
import random
import re
import string
import pycountry

from urllib.parse import urlparse
from urllib.parse import urlunparse
from urllib.parse import urljoin
from django.apps import apps
from django.conf import settings
from django.contrib import auth
from django.db.utils import OperationalError, ProgrammingError
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _

from fleio.conf.models import Configuration, Option


@deconstructible
class RandomId(object):
    """
    Callable that generates a random primary key that is unique in the specified model's table.
    """

    def __init__(self, model_param):
        """:param: model - can be model name as string or model class"""
        self.model_param = model_param

    def __call__(self):
        random.seed()
        if isinstance(self.model_param, str):
            model_name = self.model_param
            try:
                model_class = apps.get_model(self.model_param)
            except LookupError as e:
                # the table does not exit
                # this was probably called during a Django migration
                # i'm applying this advice: https://code.djangoproject.com/ticket/24182#comment:2
                model_class = None
        else:
            model_class = self.model_param
            model_name = self.model_param._meta.app_label + '.' + self.model_param._meta.object_name

        scope = 'default'
        if model_name in settings.FLEIO_RANDOM_ID:
            scope = model_name
        minimum = settings.FLEIO_RANDOM_ID[scope]['MIN']
        maximum = settings.FLEIO_RANDOM_ID[scope]['MAX']
        retries = 0
        ModelClass = model_class
        rid = int()
        while True:
            rid = random.randint(minimum, maximum)
            if model_class is None:
                # database table does not exist; we're probably in a migration
                return rid
            try:
                ModelClass.objects.get(id=rid)
            except ModelClass.DoesNotExist:
                break
            except (ProgrammingError, OperationalError):
                # db table probably doesn't exist yet
                # workaround for the fact that schema migration (uselessly) tries to get the field's default value
                # ProgrammingError - for mysql
                # OperationalError - for sqllite
                return None
            retries += 1
            if retries >= settings.FLEIO_RANDOM_ID[scope]['GROW_AFTER_COLLISIONS']:
                maximum = maximum * settings.FLEIO_RANDOM_ID[scope]['GROWTH_FACTOR']
                retries = 0
        return rid


def login_without_password(request, user):
    """
    Log in a user without requiring credentials (using ``login`` from
    ``django.contrib.auth``, first finding a matching backend).
    Based on https://djangosnippets.org/snippets/1547/
    """
    if not hasattr(user, 'backend'):
        for backend in settings.AUTHENTICATION_BACKENDS:
            if user == auth.load_backend(backend).get_user(user.pk):
                user.backend = backend
                break
    if hasattr(user, 'backend'):
        return auth.login(request, user)


def random_string():
    """Generates a random string which can be used as random passwords, random user names, etc."""
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits)
                   for _ in range(random.randint(9, 15)))


def check_password_complexity(password):
    """
    Verify password strength
    8 characters length or more
    1 symbol or more or 1 digit or more
    """
    if password and isinstance(password, str):
        length_error = len(password) < 8
        digit_or_symbol = re.search(r'\d', password) is None and re.search(r"[ !#$@%&'()*+,-./[\\\]^_`{|}~" + r'"]',
                                                                           password) is None
        password_ok = not (length_error or digit_or_symbol)
    else:
        length_error = True
        digit_or_symbol = True
        password_ok = False

    return {
        'password_ok': password_ok,
        _('It should be at least 8 characters long.'): length_error,
        _('It should contain at least one digit or symbol.'): digit_or_symbol,
    }


def get_countries():
    countries = [(entry.alpha_2, entry.name) for entry in pycountry.countries]
    result = []
    for country in countries:

        result.append(
            {
                'label': country[1],
                'value': country[0],
                'state_required': settings.STATE_REQUIRED_FOR_COUNTRY.get(country[0], True),
            }
        )
    return result


def get_user_changed_values(instance, values):
    """Procedure used to detect changes of attributes in a Django AppUser model

    instance: object, fleio.core.models.AppUser
    values: dict, mapping of serialized, valid values coming from fleio.core.serializers.UpdateUserSerializer

    :returns: list; a list of three item tuples, where each tuple has the form (field_name, old_value, new_value)
    """

    # TODO(Marius): rename this procedure and change it's body to work for any model in the project after a list of
    # required logs is built
    changed_items = []

    for key in values:
        if key == 'password':
            continue
        old_value = getattr(instance, key, None)
        new_value = values[key]

        if old_value and old_value != new_value:
            changed_items.append((key, old_value, new_value))

    return changed_items


def format_for_log(items):
    """Procedure used to format a text for a logging signal based on a list of items.

    items: list, list of three item tuples, i.e (db_field_name, old_value, new_value)

    :returns str, formatted string in the form of 'field_name: FROM <old_value> TO <new_value>, ...'
    """

    return ', '.join(['{0}: from "{1}" to "{2}"'.format(field, old_value, new_value)
                      for field, old_value, new_value in items])


def is_white_label_license():
    try:
        from fleio.core.loginview import get_license_info
        license_info = json.loads(get_license_info())
        return license_info.get('White label', False)
    except (ImportError, Exception):
        return False


def _fleio_parse_url(url, scheme='http'):
    """Return the url with scheme included and with a trailing slash always appended"""
    parsed = urlparse(url)
    # Add ending slash if missing
    if url and url[-1:] != '/':
        url += '/'
    if not parsed.scheme:
        url = '{}://{}'.format(scheme, url)
    # Add scheme if missing
    return urlparse(url)


def fleio_parse_url(url, scheme='http'):
    """Return a parsed url with a trailing slash and scheme if missing"""
    parsed = _fleio_parse_url(url=url, scheme=scheme)
    return urlunparse(parsed)


def fleio_join_url(url, path, scheme='http'):
    """Join two parts, the first one always assumed to be a base url"""
    str_url = fleio_parse_url(url=url, scheme=scheme)
    return urljoin(base=str_url, url=path.lstrip('/'))


def get_default_configuration_field_value(field_name: str):
    """Gets the value of a given field from the default configuration"""
    # TODO: see if it is ok to get default configuration without reseller
    default_configuration = Configuration.objects.default()
    if default_configuration:
        config_option = Option.objects.filter(
            configuration=default_configuration, field=field_name
        ).first()  # type: Option
        if config_option:
            return config_option.value
    return None


def is_valid_ascii(value: str):
    try:
        value.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True
