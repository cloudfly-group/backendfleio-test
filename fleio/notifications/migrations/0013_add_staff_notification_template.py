from django.db import migrations


STAFF_NEW_ORDER_NOTIFICATION_BODY = """
<p>A new order has been placed by client {{ variables.client_name }}({{ variables.client_id }})</p>
<p>To see the order click on this link <a href="{{ variables.frontend_url }}/staff/billing/orders/{{ variables.order_id }}">{{ variables.frontend_url }}/staff/billing/orders/{{ variables.order_id }}</a>.</p>
<p>For client details click on this link <a href="{{ variables.frontend_url }}/staff/clients/{{ variables.client_id }}">{{ variables.frontend_url }}/staff/clients/{{ variables.client_id }}</a>.</p>

"""

STAFF_NEW_ORDER_NOTIFICATION_TITLE = 'New order created'

STAFF_NEW_PAYMENT_NOTIFICATION_BODY = """
<p>A new payment has been made by client: {{ variables.client_name }} ({{ variables.client_id }})</p>
<p>To see the payment details click on this link <a href="{{ variables.frontend_url }}/staff/billing/journal/{{ variables.journal_id }}">{{ variables.frontend_url }}/staff/billing/journal/{{ variables.journal_id }}</a>.</p>
<p>For client details click on this link <a href="{{ variables.frontend_url }}/staff/clients/{{ variables.client_id }}">{{ variables.frontend_url }}/staff/clients/{{ variables.client_id }}</a>.</p>

"""

STAFF_NEW_PAYMENT_NOTIFICATION_TITLE = 'New payment received'


def add_staff_category(apps):
    category = apps.get_model('notifications.Category')
    return category.objects.create(name='staff', description='Staff notifications')


def add_staff_notification_templates(apps, schema_editor):
    staff_category = add_staff_category(apps=apps)
    nt_model = apps.get_model('notifications.NotificationTemplate')
    nt_model.objects.create(
        name='staff.new_order',
        category=staff_category,
        title=STAFF_NEW_ORDER_NOTIFICATION_TITLE,
        content=STAFF_NEW_ORDER_NOTIFICATION_BODY,
    )
    nt_model.objects.create(
        name='staff.new_payment',
        category=staff_category,
        title=STAFF_NEW_PAYMENT_NOTIFICATION_TITLE,
        content=STAFF_NEW_PAYMENT_NOTIFICATION_BODY,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0012_notificationtemplate_disable_notification'),
    ]

    operations = [
        migrations.RunPython(add_staff_notification_templates),
    ]
