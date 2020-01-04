from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response
from fleio.core.drf import EndUserOnly
from fleio.billing.models import Invoice
from .conf import conf


@api_view(http_method_names=['POST'])
@permission_classes((EndUserOnly, ))
def callback(request):
    return Response({'ok': 'ok'})


@api_view(http_method_names=['GET'])
@permission_classes((EndUserOnly, ))
def config(request):
    order_id = request.query_params.get('order')
    if order_id is None:
        raise APIException(detail="An 'order' parameter is required", code=400)
    try:
        inv = Invoice.objects.get(pk=order_id, client__in=request.user.clients.all())
    except Invoice.DoesNotExist:
        raise NotFound(detail='Invoice {} does not exist'.format(order_id))
    if inv.balance <= 0:
        raise APIException(detail='The order balance cannot be negative', code=400)
    return Response({'key': conf.public_key,
                     'order_id': order_id,
                     'amount': inv.balance,
                     'currency': inv.currency.pk})
