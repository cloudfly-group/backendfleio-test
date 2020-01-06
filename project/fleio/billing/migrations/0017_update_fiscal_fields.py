from django.db import migrations

from fleio.billing.settings import BillingSettings
from fleio.conf.types import Boolean


def update_fiscal_fields(apps, schema_editor):
    del schema_editor

    configuration_mode = apps.get_model('conf', 'Configuration')

    for conf_record in configuration_mode.objects.all():
        # Field `paid_invoice_sequential_numbering` is no longer in BillingSettings class
        # let's manually deserialize from db
        billing_settings = BillingSettings(configuration_id=conf_record.id)
        try:
            paid_invoice_sequential_numbering =\
                Boolean().deserialize(billing_settings.get_options()['paid_invoice_sequential_numbering'])
        except KeyError:
            # it's a clean new database that is missing `paid_invoice_sequential_numbering` setting
            # set default value
            paid_invoice_sequential_numbering = True

        for client in conf_record.client_set.all():
            for invoice in client.invoice_set.all():
                if paid_invoice_sequential_numbering is True:
                    invoice.is_fiscal = True
                    invoice.fiscal_date = invoice.issue_date
                    invoice.fiscal_due_date = invoice.due_date
                    invoice.save(update_fields=['is_fiscal', 'fiscal_date', 'fiscal_due_date'])


def revert_update_fiscal_fields(apps, schema_editor):
    del schema_editor

    invoice_model = apps.get_model('billing', 'Invoice')
    invoice_model.objects.all().update(is_fiscal=False, fiscal_date=None, fiscal_due_date=None)


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0016_add_fiscal_invoice_fields'),
    ]

    operations = [
        migrations.RunPython(update_fiscal_fields, revert_update_fiscal_fields),
    ]
