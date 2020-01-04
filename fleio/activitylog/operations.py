from ipware.ip import get_ip

from fleio.activitylog.models import Log
from fleio.activitylog.models import LogCategory
from fleio.activitylog.models import LogClass
from fleio.core.features import active_features


def fetch_log_category(name):
    log_category, created = LogCategory.objects.get_or_create(name=name)
    return log_category


def _fetch_log_class(category, logclass_name, logclass_type):
    """Gets or creates a log class with a specific name (e.g staff.logged.in) for a specific category (e.g core)
    category: fleio.activitylog.models.LogCategory model object
    logclass_name: fleio.activitylog.models.LogClass.name field object
    logclass_type: fleio.activitylog.models.LogClass.type field object (info or error)

    :returns a log class model object
    """

    log_class, _ = LogClass.objects.get_or_create(category=category, name=logclass_name, type=logclass_type)
    return log_class


def add_request_log(category, logclass_name, logclass_type, **kwargs):
    user = kwargs.pop('user', None)
    request = kwargs.pop('request', None)
    kwargs.pop('signal', None)

    if request:
        ip = get_ip(request)
        if hasattr(request, 'impersonator'):
            kwargs['impersonator'] = request.impersonator.username
            kwargs['impersonator_id'] = request.impersonator.pk
    else:
        ip = None

    add_log(category, logclass_name, logclass_type, user=user, ip=ip, **kwargs)


def add_log(category, logclass_name, logclass_type, user=None, ip=None, **kwargs):
    log_class = _fetch_log_class(category, logclass_name, logclass_type)

    if active_features.is_enabled('demo'):
        # do not record visitors IP in demo mode
        ip = None

    Log.objects.create(user=user, ip=ip, log_class=log_class, parameters=kwargs)
