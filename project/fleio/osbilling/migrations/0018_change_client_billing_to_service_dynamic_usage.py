from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0020_product_hide_services'),
        ('osbilling', '0017_add_services_to_client_billing'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ClientBilling',
            new_name='ServiceDynamicUsage',
        ),
        migrations.RemoveField(
            model_name='servicedynamicusage',
            name='client',
        ),
        migrations.AlterField(
            model_name='clientbillinghistory',
            name='client_billing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='billing_cycle_history',
                                    to='osbilling.ServiceDynamicUsage'),
        ),
        migrations.RenameModel(
            old_name='ClientBillingHistory',
            new_name='ServiceDynamicUsageHistory',
        ),
        migrations.RenameField(
            model_name='servicedynamicusagehistory',
            old_name='client_billing',
            new_name='service_dynamic_usage',
        ),
        migrations.DeleteModel(
            name='ClientOpenStackMonthlyReporting',
        ),
        migrations.AlterField(
            model_name='servicedynamicusage',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_dynamic_usage',
                                    to='osbilling.PricingPlan'),
        ),
    ]
