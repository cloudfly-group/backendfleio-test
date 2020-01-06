from django.db import migrations

STAFF_TICKET_OPENED_NT_NAME = 'ticket.staff.opened'
STAFF_TICKET_REPLY_NT_NAME = 'ticket.staff.reply'
STAFF_TICKET_CLOSED_NT_NAME = 'ticket.staff.closed'
ENDUSER_TICKET_OPENED_NT_NAME = 'ticket.enduser.opened'
ENDUSER_TICKET_REPLY_NT_NAME = 'ticket.enduser.reply'
ENDUSER_TICKET_CLOSED_NT_NAME = 'ticket.enduser.closed'

NEW_TICKETS_NT_TITLE = '[#{{ variables.ticket_id }}]: {{ variables.ticket_title }}'

STAFF_TICKET_OPENED_NEW_NT_CONTENT = """<p>Hello!</p>
<p>Ticket <a href="{{ variables.ticket_url }}">#{{ variables.ticket_id }}</a> was successfully opened.</p>
<p>Ticket body:</p>
<div>{{ variables.ticket_body }}</div>"""

STAFF_TICKET_REPLY_NEW_NT_CONTENT = """<p>A reply has been added to ticket 
<a href="{{ variables.ticket_url }}">#{{ variables.ticket_id }}</a> by {{ variables.ticket_update_owner }}.</p>
<p>Message:</p>
<div>{{ variables.ticket_update_body }}</div>"""

STAFF_TICKET_CLOSED_NEW_NT_CONTENT = """<p>Hello!</p>
<p>Ticket <a href="{{ variables.ticket_link }}">#{{ variables.ticket_id }}</a> was closed.</p>
<p>Thank you.</p>"""

ENDUSER_TICKET_OPENED_NT_CONTENT = """<p>Hello!</p>
<p>Ticket <a href="{{ variables.ticket_url }}">#{{ variables.ticket_id }}</a> was successfully opened.</p>
<p>Ticket body:</p>
<div>{{ variables.ticket_body }}</div>"""

ENDUSER_TICKET_REPLY_NT_CONTENT = """<p>A reply has been added to ticket 
<a href="{{ variables.ticket_url }}">#{{ variables.ticket_id }}</a> by {{ variables.ticket_update_owner }}.</p>
<p>Message:</p>
<div>{{ variables.ticket_update_body }}</div>"""

ENDUSER_TICKET_CLOSED_NT_CONTENT = """<p>Hello!</p>
<p>Ticket <a href="{{ variables.ticket_url }}">#{{ variables.ticket_id }}</a> was closed.</p>
<p>Thank you.</p>"""


def rename_ticketing_category(apps, schema_editor):
    category_model_class = apps.get_model('notifications.Category')
    tickets_category = category_model_class.objects.get(name='ticketing')
    tickets_category.name = 'ticket'
    tickets_category.save()


def edit_old_notifications(apps, schema_editor):
    nt_model = apps.get_model('notifications.NotificationTemplate')
    # rename ticketing.ticket.opened to ticket.staff.opened
    staff_ticket_opened_nt = nt_model.objects.filter(name='ticketing.ticket.opened')
    for notification_template in staff_ticket_opened_nt:
        notification_template.name = STAFF_TICKET_OPENED_NT_NAME
        notification_template.save()
    # rename ticketing.ticket.reply to ticket.staff.reply
    staff_ticket_reply_nt = nt_model.objects.filter(name='ticketing.ticket.reply')
    for notification_template in staff_ticket_reply_nt:
        notification_template.name = STAFF_TICKET_REPLY_NT_NAME
        notification_template.save()
    # rename ticketing.ticket.closed to ticket.staff.closed
    staff_ticket_closed_nt = nt_model.objects.filter(name='ticketing.ticket.closed')
    for notification_template in staff_ticket_closed_nt:
        notification_template.name = STAFF_TICKET_CLOSED_NT_NAME
        notification_template.save()

    # edit old default ticket notification templates content and title
    staff_ticket_opened_nt = nt_model.objects.filter(name=STAFF_TICKET_OPENED_NT_NAME, language='en').first()
    if staff_ticket_opened_nt:
        staff_ticket_opened_nt.title = NEW_TICKETS_NT_TITLE
        staff_ticket_opened_nt.content = STAFF_TICKET_OPENED_NEW_NT_CONTENT
        staff_ticket_opened_nt.save()
    staff_ticket_reply_nt = nt_model.objects.filter(name=STAFF_TICKET_REPLY_NT_NAME, language='en').first()
    if staff_ticket_reply_nt:
        staff_ticket_reply_nt.title = NEW_TICKETS_NT_TITLE
        staff_ticket_reply_nt.content = STAFF_TICKET_REPLY_NEW_NT_CONTENT
        staff_ticket_reply_nt.save()
    staff_ticket_closed_nt = nt_model.objects.filter(name=STAFF_TICKET_CLOSED_NT_NAME, language='en').first()
    if staff_ticket_closed_nt:
        staff_ticket_closed_nt.title = NEW_TICKETS_NT_TITLE
        staff_ticket_closed_nt.content = STAFF_TICKET_CLOSED_NEW_NT_CONTENT
        staff_ticket_closed_nt.save()


def add_enduser_ticket_notification_templates(apps, schema_editor):
    category_model_class = apps.get_model('notifications.Category')
    tickets_category = category_model_class.objects.get(name='ticket')
    nt_model = apps.get_model('notifications.NotificationTemplate')
    nt_model.objects.create(name=ENDUSER_TICKET_OPENED_NT_NAME,
                            category=tickets_category,
                            title=NEW_TICKETS_NT_TITLE,
                            content=ENDUSER_TICKET_OPENED_NT_CONTENT)
    nt_model.objects.create(name=ENDUSER_TICKET_REPLY_NT_NAME,
                            category=tickets_category,
                            title=NEW_TICKETS_NT_TITLE,
                            content=ENDUSER_TICKET_REPLY_NT_CONTENT)
    nt_model.objects.create(name=ENDUSER_TICKET_CLOSED_NT_NAME,
                            category=tickets_category,
                            title=NEW_TICKETS_NT_TITLE,
                            content=ENDUSER_TICKET_CLOSED_NT_CONTENT)


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0007_add_openstack_related_notification_templates'),
    ]

    operations = [
        migrations.RunPython(rename_ticketing_category),
        migrations.RunPython(edit_old_notifications),
        migrations.RunPython(add_enduser_ticket_notification_templates),
    ]
