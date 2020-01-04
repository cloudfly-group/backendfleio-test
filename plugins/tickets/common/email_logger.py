import os
import sys
import logging
import uuid

from django.conf import settings
from django.utils.timezone import now as utcnow

LOG = logging.getLogger(__name__)


class EmailLogger:

    @staticmethod
    def save_email_message(email_message):
        """saves incoming email on disk"""
        ticket_emails_location = getattr(settings, 'LOGGED_TICKET_EMAILS_LOCATION', '/var/fleio/ticket_emails')
        try:
            if not os.path.exists(ticket_emails_location):
                parent_dir = os.path.dirname(ticket_emails_location)
                parent_stat = os.stat(parent_dir)
                os.mkdir(ticket_emails_location)
                stats = os.stat(ticket_emails_location)
                if stats.st_uid != parent_stat.st_uid:
                    os.chown(ticket_emails_location, parent_stat.st_uid, parent_stat.st_gid)

            content_size = sys.getsizeof(email_message)
            # Check if size is not bigger than the limit
            if content_size > getattr(settings, 'MAX_LOGGED_TICKET_EMAIL_SIZE', 104857600):
                LOG.warning('Email file size is bigger than the allowed size, ignoring')
                return
            statvfs = os.statvfs(ticket_emails_location)
            free_space = statvfs.f_frsize * statvfs.f_bavail
            if free_space < getattr(settings, 'FREE_DISK_SPACE_LIMIT') or free_space < content_size:
                LOG.error('There is not enough free space on the disk to save the email, ignoring')
                return

            now = utcnow()
            year = now.year
            month = now.month
            day = now.day

            current_ticket_email_location = '{}/{}-{}-{}'.format(
                ticket_emails_location, year, month, day
            )
            if not os.path.exists(current_ticket_email_location):
                parent_dir = os.path.dirname(current_ticket_email_location)
                parent_stat = os.stat(parent_dir)
                os.mkdir(current_ticket_email_location)
                stats = os.stat(current_ticket_email_location)
                if stats.st_uid != parent_stat.st_uid:
                    os.chown(current_ticket_email_location, parent_stat.st_uid, parent_stat.st_gid)

            hour = now.hour
            minute = now.minute
            random_uuid = uuid.uuid4()
            filename = '{}/{}-{}-{}-{}-{}-{}.eml'.format(
                current_ticket_email_location, year, month, day, hour, minute, random_uuid
            )
            with open(filename, 'w') as fp:
                fp.write(email_message)

        except Exception as e:
            LOG.error('An error occurred when trying to log received ticket email: {}'.format(str(e)))
