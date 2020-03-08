# Generated by Django 2.1.2 on 2018-10-30 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0004_productgroup_visible'),
    ]

    operations = [
        migrations.AddField(
            model_name='configurableoption',
            name='visible',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='configurableoption',
            name='status',
            field=models.CharField(choices=[('public', 'Public'), ('private', 'Private'), ('retired', 'Retired')], db_index=True, max_length=8),
        ),
    ]