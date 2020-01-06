from django.db import migrations, transaction, utils


def update_resources_with_details(apps, schema_editor):
    """Add osbilling resources with attributes and metrics"""
    resource = apps.get_model("osbilling", "BillingResource")
    instance_definition = {"attributes": [{"type": "string",
                                           "name": "availability_zone"},
                                          {"type": "string",
                                           "name": "instance_type"},
                                          {"type": "string",
                                           "name": "display_name"},
                                          {"type": "string",
                                           "name": "cell_name"},
                                          {"type": "datetime",
                                           "name": "launched_at"},
                                          {"type": "string",
                                           "name": "state"},
                                          {"type": "integer",
                                           "name": "vcpus"},
                                          {"type": "integer",
                                           "name": "root_gb",
                                           "value_size": 'g'},
                                          {"value_size": "m",
                                           "name": "memory_mb",
                                           "type": "integer"},
                                          {"type": "string",
                                           "name": "os_type"},
                                          {"type": "string",
                                           "name": "os_version"},
                                          {"type": "string",
                                           "name": "instance_id"},
                                          {"type": "string",
                                           "name": "tenant_id"},
                                          {"type": "string",
                                           "name": "host"},
                                          {"type": "integer",
                                           "name": "ephemeral_gb",
                                           "value_size": "g"},
                                          {"type": "string",
                                           "name": "region"}]}
    image_definition = {"attributes": [{"value_size": "b",
                                        "type": "integer",
                                        "name": "size"},
                                       {"type": "datetime",
                                        "name": "created_at"},
                                       {"type": "datetime",
                                        "name": "updated_at"},
                                       {"type": "string",
                                        "name": "disk_format"},
                                       {"type": "string",
                                        "name": "visibility"},
                                       {"type": "string",
                                        "name": "status"},
                                       {"type": "string",
                                        "name": "name"},
                                       {"type": "string",
                                        "name": "region"}]}

    volume_definition = {"attributes": [{"value_size": "g",
                                         "type": "integer",
                                         "name": "size"},
                                        {"type": "string",
                                         "name": "availability_zone"},
                                        {"type": "datetime",
                                         "name": "created_at"},
                                        {"type": "string",
                                         "name": "volume_type"},
                                        {"type": "string",
                                         "name": "display_name"},
                                        {"type": "string",
                                         "name": "region"}]}

    swift_metrics = {
        "metrics": [
            {
                "rescale_to": "g",
                "name": "storage.objects.incoming.bytes",
                "aggregation": "sum",
                "reaggregation": "sum",
                "granularity": 300,
                "unit": "b"
            },
            {
                "rescale_to": "g",
                "name": "storage.objects.outgoing.bytes",
                "aggregation": "sum",
                "reaggregation": "sum",
                "granularity": 300,
                "unit": "b"
            },
            {
                "name": "storage.api.requests",
                "aggregation": "sum",
                "reaggregation": "sum",
                "granularity": 300
            },
            {
                "name": "storage.objects",
                "aggregation": "mean",
                "reaggregation": "mean",
                "granularity": 300
            },
            {
                "name": "storage.objects.containers",
                "aggregation": "mean",
                "reaggregation": "mean",
                "granularity": 300
            },
            {
                "rescale_to": "g",
                "name": "storage.objects.size",
                "aggregation": "mean",
                "reaggregation": "mean",
                "granularity": 300,
                "unit": "b"
            }
        ]
    }

    network_metrics = {
        "metrics": [
            {
                "rescale_to": "g",
                "name": "bandwidth",
                "aggregation": "sum",
                "reaggregation": "sum",
                "granularity": 300,
                "unit": "b"
            },
            {
                "name": "ip.floating",
                "aggregation": "mean",
                "reaggregation": "mean",
                "granularity": 300
            }
        ]
    }

    try:
        with transaction.atomic():
            resource.objects.filter(name='instance').update(definition=instance_definition)
            resource.objects.filter(name='image').update(definition=image_definition)
            resource.objects.filter(name='volume').update(definition=volume_definition)
            resource.objects.filter(name='network').update(definition=network_metrics)
            resource.objects.filter(name='swift_account').update(definition=swift_metrics)
    except utils.IntegrityError:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('osbilling', '0007_add_swift_resources'),
    ]

    operations = [
        migrations.RunPython(update_resources_with_details),
    ]
