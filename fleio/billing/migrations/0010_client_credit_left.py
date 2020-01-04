from django.db import migrations, models
import django.db.models.deletion
import fleio.core.models.models
from django.db import migrations, models


def update_credit_left_on_journal_entries(apps, schema_editor):
    journal_model = apps.get_model('billing', 'Journal')
    client_model = apps.get_model('core', 'Client')
    clients = client_model.objects.all()
    for client in clients:
        client_main_credit_account = client.credits.filter(currency=client.currency).first()
        if client_main_credit_account:
            last_journal = journal_model.objects.filter(
                models.Q(client_credit=client_main_credit_account) | models.Q(invoice__client=client)
            ).order_by('date_added').last()  # get the oldest journal entry
            if last_journal:
                last_journal.client_credit_left = client_main_credit_account.amount
                try:
                    last_journal.client_credit_left_currency = client_main_credit_account.currency
                except (Exception, client_main_credit_account.currency.RelatedObjectDoesNotExist) as e:
                    last_journal.client_credit_left = None
                last_journal.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_client_extra_statuses'),
        ('billing', '0009_service_domain_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='journal',
            name='client_credit_left',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=14, null=True),
        ),
        migrations.AddField(
            model_name='journal',
            name='client_credit_left_currency',
            field=models.ForeignKey(default=fleio.core.models.get_default_currency, null=True,
                                    on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='journal_credit_left_currencies',
                                    to='core.Currency'),
        ),
        migrations.RunPython(update_credit_left_on_journal_entries),
    ]
