# flake8: NOQA
from __future__ import unicode_literals

import logging
import os
import six
import sys
import threading
from datetime import timedelta
from os import environ
from os.path import abspath, dirname

import django
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

current_path = dirname(abspath(__file__))
fleio_path = dirname(dirname(dirname(current_path)))

sys.path.append(fleio_path)
environ.setdefault("DJANGO_SETTINGS_MODULE", "fleio.settings")
django.setup()

from fleio.openstack import utils
from fleio.openstack.api.nova import nova_client
from fleio.openstack.api.glance import glance_client
from fleio.openstack.api.session import get_session
from fleio.osbackup.models import OpenStackBackupSchedule, OpenStackBackupLog
from fleio.openstack.settings import plugin_settings

USER_INPUT_TIMEOUT = 10
current_time = timezone.now()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('Starting all backups before {}'.format(current_time.strftime('%Y-%m-%d %H:%M:%S')))

cache_dict = dict()
os_auth_cache = utils.OSAuthCache(request_session=cache_dict)


def admin_session():
    return get_session(auth_url=plugin_settings.AUTH_URL,
                       project_id=plugin_settings.user_project_id,
                       project_domain_id=plugin_settings.project_domain_id,
                       admin_username=plugin_settings.USERNAME,
                       admin_password=plugin_settings.PASSWORD,
                       admin_domain_id=plugin_settings.user_domain_id,
                       cache=os_auth_cache,
                       timeout=plugin_settings.TIMEOUT)


def custom_session(project_id):
    return get_session(auth_url=plugin_settings.AUTH_URL,
                       project_id=project_id,
                       project_domain_id=plugin_settings.project_domain_id,
                       admin_username=plugin_settings.USERNAME,
                       admin_password=plugin_settings.PASSWORD,
                       admin_domain_id=plugin_settings.user_domain_id,
                       cache=os_auth_cache,
                       timeout=plugin_settings.TIMEOUT)


def run_backup(time_to_execute):
    # TODO(MARIUS): implement command line arguments (recognisable flags like --force/-f)
    # TODO(MARIUS): don't backup schedules from db that have already been executed (they pass the filter condition now)
    # TODO(MARIUS): check backup types and execute the backups based on that, for accuracy
    """
    :param time_to_execute: The time at which the procedure will be executed.

    Scenario 1 (auto-run):
        - an external automatic process (cron for linux, windows task scheduler for windows) will be set to execute this
          script, in which :param time_to_execute: will be the time that the external process was set to run
          e.g (5:00 AM, daily / weekly / etc.)

    Scenario 2 (manual-run):
        - script is run manually, in which case :param time_to_execute: will be the time at which the script is executed

    All backups that are scheduled BEFORE the :param time_to_execute: are going to be executed.
    """
    # default_session = admin_session()
    backups_to_execute = OpenStackBackupSchedule.objects.filter(run_at__lt=time_to_execute)
    total_backups = len(backups_to_execute)
    backups_executed = 0
    backups_failed = []
    session_map = dict(
        # stores sessions based on project_id
    )
    for backup in backups_to_execute:
        instance_region = backup.instance.region
        project_id = backup.instance.project_id
        # use the session related to the instance project_id
        new_session = session_map.get(project_id, None)
        if not new_session:
            new_session = custom_session(project_id=project_id)
            session_map[project_id] = new_session  # store the session in case we need it later
        gc = glance_client(api_session=new_session, region_name=instance_region)
        nc = nova_client(api_session=new_session, region_name=instance_region)
        nc.servers.backup(server=backup.instance.id, backup_name=backup.backup_name,
                          backup_type=backup.backup_type, rotation=backup.rotation)
        if len(list(gc.images.list(filters={'name': backup.backup_name}))) > 0:
            backups_executed += 1
        else:
            backups_failed.append(backup.instance.id)
            logger.error(e)
            logger.info(
                'Cannot perform backup on instance {}, instance currently under a task state.'
                .format(backup.instance.id)
            )
    time_to_execute = time_to_execute.strftime('%Y-%m-%d %H:%M:%S')

    if not backups_failed:
        msg = _('{executed} out of {total} backups were created successfully before {time_to_execute}').format(
            executed=backups_executed, total=total_backups, time_to_execute=time_to_execute)
    else:
        msg = _('Could not backup the following virtual machines: {failed}\n').format(backups_failed)
        msg += _('Backed up {executed} out of {total} virtual machines').format(
            executed=backups_executed, total=total_backups)
    OpenStackBackupLog.objects.create()
    return msg


def timeout_termination(code, seconds=None, trigger=None):
    if trigger:
        msg = 'Done!'
    else:
        msg = _('No input or wrong input received for the past {} seconds, canceling backup execution').format(seconds)
    print(msg)
    os._exit(code)


if __name__ == "__main__":
    if six.PY34:
        raw_input = input  # NOTE(tomo): raw_input from py2 renamed to input in py3
    try:
        past_hours = current_time - timedelta(hours=3)
        past_backups = OpenStackBackupLog.objects.filter(executed_at__range=(past_hours, current_time))

        if past_backups:
            timer = threading.Timer(USER_INPUT_TIMEOUT, timeout_termination, [0, USER_INPUT_TIMEOUT])
            timer.start()
            latest_backup = past_backups.latest('executed_at')
            pretty_format = latest_backup.executed_at.strftime('%Y-%m-%d %H:%M:%S')
            msg_topic = _('Backups were already run at {}.\n').format(pretty_format)
            msg_body = _('Warning: If no input or wrong input will be provided in the next {} seconds,'
                         ' backup execution will be canceled').format(USER_INPUT_TIMEOUT)
            print('{}{}'.format(msg_topic, msg_body))
            while True:
                user_input = raw_input(_('Do you wish to backup again? [Y/N]: ')).lower()
                values = {'y': True, 'yes': True, 'n': False, 'no': False}

                if user_input in values:
                    if user_input == 'no' or user_input == 'n':
                        timeout_termination(code=0, trigger=True)
                    else:
                        timer.cancel()
                        logger.info(run_backup(current_time))
                        timeout_termination(code=0, trigger=True)
                else:
                    msg = _('{} not recognized, please use one of the following: y, yes, n, no').format(user_input)
                    print(msg)

        else:
            logger.info(run_backup(current_time))

    except Exception as e:
        logger.error(e)
