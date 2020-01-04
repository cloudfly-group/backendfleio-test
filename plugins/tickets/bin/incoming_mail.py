import logging
from os import environ
from os.path import abspath, dirname, isfile
import sys

import django

current_path = dirname(abspath(__file__))
fleio_path = dirname(dirname(dirname(current_path)))

sys.path.append(fleio_path)
environ.setdefault("DJANGO_SETTINGS_MODULE", "fleio.settings")
django.setup()

LOG = logging.getLogger('incoming_mail')

from plugins.tickets.common.email_processor import EmailProcessor  # noqa
from plugins.tickets.common.tickets_utils import TicketUtils  # noqa


def run():
    mail_contents = None
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        if isfile(input_file):
            mail_contents = open(sys.argv[1]).read()
    else:
        mail_contents = sys.stdin.read()

    if mail_contents:
        received_message = EmailProcessor.parse_email_message(message=mail_contents)
        if received_message:
            TicketUtils.create_or_update_ticket_from_received_email(received_email=received_message)


if __name__ == '__main__':
    run()
