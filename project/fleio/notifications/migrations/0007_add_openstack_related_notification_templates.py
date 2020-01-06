from django.db import migrations


OPENSTACK_NOTIFICATION = """Hello,
<br>
{{variables.custom_message}}
<br>
Message received from openstack: {{variables.openstack_message}}
<br> 
Thanks.

"""


def add_openstack_category(apps, schema_editor):
    category = apps.get_model('notifications.Category')
    category.objects.create(name='openstack', description='Openstack related messages')


def add_openstack_template(apps, schema_editor):
    category = apps.get_model('notifications.Category')
    openstack_category = category.objects.get(name='openstack')
    nt_model = apps.get_model('notifications.NotificationTemplate')
    nt_model.objects.create(name='openstack.error',
                            category=openstack_category,
                            title='There was an error when trying to {{variables.action_performed}}',
                            content=OPENSTACK_NOTIFICATION)


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0006_add_ticketing_system_notification_templates'),
    ]

    operations = [
        migrations.RunPython(add_openstack_category),
        migrations.RunPython(add_openstack_template),
    ]
