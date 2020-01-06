from rest_framework import serializers

from fleio.billing.models import Order, OrderItem

from fleio.core.clients.serializers import ClientMinSerializer
from fleio.core.serializers import UserMinSerializer


from fleiostaff.billing.invoicing.serializers import StaffInvoiceBriefSerializer

#  NOTE(tomo): Replaced this serializer created for StaffOrderSerializer.cart field
# class StaffOrderItemSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=255)
#     description = serializers.CharField(max_length=1024)
#     cycle_display = serializers.CharField(max_length=255)


class StaffOrderItemSerializer(serializers.ModelSerializer):
    service = serializers.SerializerMethodField()
    link_params = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ('id', 'name', 'description', 'cycle_display', 'service', 'link_params')

    @staticmethod
    def get_service(obj):
        return getattr(getattr(obj, 'service', None), 'id', None)

    @staticmethod
    def get_link_params(order_item):
        if not order_item.service:
            return ''
        if hasattr(order_item.service, 'domain'):
            return 'pluginsDomainsDomainDetails({id: ' + str(order_item.service.domain.id) + '})'
        else:
            return 'billingServicesDetails({id: ' + str(order_item.service.id) + '})'


class StaffOrderSerializer(serializers.ModelSerializer):
    # cart = StaffOrderItemSerializer(read_only=True, many=True)  #  NOTE(tomo): remove this field
    user = UserMinSerializer(read_only=True)
    client = ClientMinSerializer(read_only=True)
    invoice = StaffInvoiceBriefSerializer(read_only=True)
    fraud_check_result = serializers.JSONField(read_only=True)
    items = StaffOrderItemSerializer(read_only=True, many=True)
    total = serializers.DecimalField(read_only=True, decimal_places=2, max_digits=12)

    class Meta:
        model = Order
        fields = '__all__'
