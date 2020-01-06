from fleio.billing.client_operations import ClientOperations
from fleio.billing.serializers import ClientCreditMinSerializer

from fleio.openstack.instances.instance_status import InstanceStatus
from fleio.openstack.models import Image, Instance, Project, Volume

from fleio.pkm.models import PublicKey


def get_summary(user):
    projects = Project.objects.filter(service__client__in=user.clients.all())
    instances = (Instance.objects.filter(project_id__in=projects.values_list('project_id'))
                 .exclude(status=InstanceStatus.DELETED).exclude(terminated_at__isnull=False))
    instance_count = instances.count()
    stopped_instance_count = instances.filter(status=InstanceStatus.STOPPED).count()
    image_count = (Image.objects.filter(project__in=projects)
                   .exclude(status='deleted').count())
    volume_count = (Volume.objects.filter(project_id__in=projects.values('project_id')).count())
    key_count = PublicKey.objects.filter(user=user).count()

    client = user.clients.first()
    client_operations = ClientOperations(client=client)

    unpaid_usage = client_operations.client_usage.unpaid_usage
    uptodate_credit = client_operations.uptodate_credit

    other_credit = client.credits.exclude(currency=client.currency)

    summary = {
        'credits': ClientCreditMinSerializer(instance=other_credit, many=True).data,
        'uptodate_credit': uptodate_credit,
        'billing_currency': client.currency.code,
        'unpaid_usage': unpaid_usage,
        'instances': instance_count,
        'stopped_instances': stopped_instance_count,
        'images': image_count,
        'volumes': volume_count,
        'pkm': key_count
    }
    return summary
