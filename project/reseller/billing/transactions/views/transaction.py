from django.db.models.deletion import ProtectedError
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.response import Response

from fleio.billing.invoicing.tasks import invoice_delete_transaction
from fleio.billing.models import Transaction
from fleio.core.drf import ResellerOnly
from fleio.reseller.utils import user_reseller_resources
from reseller.billing.transactions.serializers.transaction import ResellerTransactionSerializer


class ResellerTransactionViewSet(viewsets.ModelViewSet):
    permission_classes = (ResellerOnly,)
    serializer_class = ResellerTransactionSerializer
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filter_fields = ('invoice__client_id',)

    def get_queryset(self):
        reseller_resources = user_reseller_resources(self.request.user)
        return Transaction.objects.filter(
            invoice__client__reseller_resources=reseller_resources
        ).order_by('-date_initiated')

    def destroy(self, request, *args, **kwargs):
        transaction = self.get_object()  # type: Transaction
        try:
            invoice_delete_transaction(transaction.id)
        except ProtectedError:
            return Response(
                status=403,
                data={'detail': _('Cannot delete refunded transaction, delete refund transaction first')}
            )

        return Response({'detail': _('Ok')})
