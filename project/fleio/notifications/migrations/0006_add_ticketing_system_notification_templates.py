from django.db import migrations


TICKET_OPENED = """Hello,

Ticket {{ variables.ticket_id }} was successfully opened. Thank you.

Ticket description: {{ variables.ticket_description }}

"""

TICKET_REPLY = """Hello,

A reply has been added to the ticket {{ variables.ticket_id }} by {{ variables.ticket_update_owner }}.

Message: {{ variables.ticket_update_description }}

"""

TICKET_CLOSED = """Hello,

Ticket {{ variables.ticket_id }} was closed.

Thank you.

"""


def add_ticketing_category(apps, schema_editor):
    category = apps.get_model('notifications.Category')
    category.objects.create(name='ticketing', description='Ticketing system related messages')


def add_ticketing_templates(apps, schema_editor):
    category = apps.get_model('notifications.Category')
    ticketing_category = category.objects.get(name='ticketing')
    nt_model = apps.get_model('notifications.NotificationTemplate')
    nt_model.objects.create(name='ticketing.ticket.opened',
                            category=ticketing_category,
                            title='Ticket {{ variables.ticket_id }} {{ variables.ticket_title }}',
                            content=TICKET_OPENED)
    nt_model.objects.create(name='ticketing.ticket.reply',
                            category=ticketing_category,
                            title='Ticket {{ variables.ticket_id }} {{ variables.ticket_title }}',
                            content=TICKET_REPLY)
    nt_model.objects.create(name='ticketing.ticket.closed',
                            category=ticketing_category,
                            title='Ticket {{ variables.ticket_id }} {{ variables.ticket_title }}',
                            content=TICKET_CLOSED)


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0005_allow_notifications_without_client'),
    ]

    operations = [
        migrations.RunPython(add_ticketing_category),
        migrations.RunPython(add_ticketing_templates),
    ]
