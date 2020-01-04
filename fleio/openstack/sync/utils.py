from __future__ import unicode_literals
import logging
import time
from django.db import connection, OperationalError

LOG = logging.getLogger(__name__)


def retry_on_deadlock(f):
    # FIXME(tomo): Retry on mysql wait timeout (reopen connection)
    retry_interval = 1
    max_retries = 10

    def decorator(*args, **kwargs):
        retries = 1
        while retries < max_retries:
            retries += 1
            try:
                return f(*args, **kwargs)
            except OperationalError as e:
                LOG.debug('Retry on {} : {}'.format(f.__name__, e))
                if retries > 2:  # FIXME(tomo): This is too much here. Try to actually find out if mysql is gone!
                    connection.close()
                time.sleep(retry_interval + retries)
        LOG.error('Giving up on retrying database transaction.')
    return decorator
