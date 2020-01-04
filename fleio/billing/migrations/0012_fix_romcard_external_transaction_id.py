from django.db import migrations


def change_external_id_and_add_int_ref_to_extra(apps, schema_editor):
    journal_model = apps.get_model('billing.Journal')
    gateway_model = apps.get_model('billing.Gateway')
    romcard_gateway = gateway_model.objects.filter(name='romcard').first()
    if romcard_gateway:
        journal_entries = journal_model.objects.filter(transaction__gateway=romcard_gateway)
        for journal_entry in journal_entries:
            transaction = journal_entry.transaction
            extra = transaction.extra
            extra['INT_REF'] = transaction.external_id
            transaction.extra = extra
            rrn = extra.get('RRN')
            if rrn:
                transaction.external_id = rrn
            transaction.save()


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0011_change_cycle_multipler_type_to_int'),
    ]

    operations = [
        migrations.RunPython(change_external_id_and_add_int_ref_to_extra),
    ]
