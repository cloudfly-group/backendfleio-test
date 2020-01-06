from django.db import migrations


SIGNUP_CONFIRM_NOTIFICATION_BODY = """<p>Hi {{ variables.first_name }},</p>
<p>To complete the registration process, click on this link <a href="{{ variables.frontend_url }}confirm-email/{{ variables.confirmation_token }}">{{ variables.frontend_url }}confirm-email/{{ variables.confirmation_token }}</a>.</p>
<p>You can also copy/paste this code in your user account: {{ variables.confirmation_token }}</p>
<p>Please note that this validation code will expire after 24h.</p>
<p>Thanks!</p>

"""

SIGNUP_CONFIRM_NOTIFICATION_TITLE = 'Confirm your account'


def add_signup_confirm_template(apps, schema_editor):
    category = apps.get_model('notifications.Category')
    account_category = category.objects.get(name='account')
    nt_model = apps.get_model('notifications.NotificationTemplate')
    nt_model.objects.create(name='account.signup.confirm',
                            category=account_category,
                            title=SIGNUP_CONFIRM_NOTIFICATION_TITLE,
                            content=SIGNUP_CONFIRM_NOTIFICATION_BODY)


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0008_edit_ticket_notification_templates'),
    ]

    operations = [
        migrations.RunPython(add_signup_confirm_template),
    ]
