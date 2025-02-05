# Generated by Django 2.2.5 on 2019-09-30 09:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_update_country_field_on_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='is_reseller',
            field=models.BooleanField(default=False, help_text='Designates whether the user is a reseller.', verbose_name='reseller status'),
        ),
        migrations.AddField(
            model_name='appuser',
            name='reseller',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='client',
            name='reseller',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clientgroup',
            name='reseller',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usergroup',
            name='reseller',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
