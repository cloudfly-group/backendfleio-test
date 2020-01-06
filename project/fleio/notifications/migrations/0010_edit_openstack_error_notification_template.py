from django.db import migrations


OPENSTACK_NOTIFICATION_BODY = """<p>{{ variables.error_message }}</p>
<p>Event ({{ variables.event_type }}) related region: {{ variables.region }}</p>
<pre>{{ variables.request_args }}</pre>

"""


def edit_openstack_error_template(apps, schema_editor):
    nt_model = apps.get_model('notifications.NotificationTemplate')
    category_model_class = apps.get_model('notifications.Category')
    openstack_category = category_model_class.objects.get(name='openstack')
    templates = nt_model.objects.filter(name='openstack.error', category=openstack_category)
    for template in templates:
        template.title = 'OpenStack error: {{ variables.error_message }}'
        template.content = OPENSTACK_NOTIFICATION_BODY
        template.save()


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0009_add_signup_confirmation_notification_template'),
    ]

    operations = [
        migrations.RunPython(edit_openstack_error_template),
    ]
