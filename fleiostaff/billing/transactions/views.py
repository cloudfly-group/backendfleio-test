from django.db.models.deletion import ProtectedError
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.response import Response

from fleio.billing.invoicing.tasks import invoice_delete_transaction
from fleio.billing.models import Transaction
from fleio.core.drf import StaffOnly
from fleiostaff.billing.transactions.serializers import StaffTransactionSerializer


class StaffTransactionViewSet(viewsets.ModelViewSet):
    permission_classes = (StaffOnly, )
    serializer_class = StaffTransactionSerializer
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filter_fields = ('invoice__client_id',)

    def get_queryset(self):
        return Transaction.objects.all().order_by('-date_initiated')

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
