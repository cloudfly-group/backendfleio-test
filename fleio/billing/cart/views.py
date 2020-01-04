from rest_framework import permissions
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.decorators import action, api_view
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from fleio.billing.settings import PricingModel
from fleio.core.drf import EndUserOnly
from fleio.billing.models import OrderItem, ProductCycle
from .serializers import OrderItemCreateOptionsSerializer
from fleio.billing.cart.serializers import cart_from_request, CartSerializer, OrderItemSerializer
from .serializers import CartProductCreateOptionsSerializer
from .utils import create_order_from_cart


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def cartview(request: Request):
    cart = cart_from_request(request, create=False)
    if cart is None:
        return Response({})
    else:
        return Response(CartSerializer(instance=cart).to_representation(cart))


@api_view(['POST'])
@permission_classes([EndUserOnly])
def create_order(request: Request):
    """Create an order form the existing Cart"""
    cart = cart_from_request(request, create=False)
    if cart is None or cart.items.count() == 0:
        return Response({'detail': 'Nothing in cart'})
    order = create_order_from_cart(cart)
    return Response({'detail': 'Order {} placed'.format(order.pk)})


class CartItemViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny, )
    serializer_class = OrderItemSerializer

    @property
    def cart(self):
        return cart_from_request(request=self.request, create=True)

    def get_queryset(self):
        cart = self.cart
        return OrderItem.objects.filter(cart=cart)

    @action(methods=['GET'], detail=False)
    def create_options(self, request):
        cart = self.cart
        serializer = OrderItemCreateOptionsSerializer(
            data=request.query_params, context={'cart': cart},
        )
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data['product']
        cycle = serializer.validated_data['cycle']
        serializer_context = {'cycle': cycle,
                              'cart': cart}
        return Response(CartProductCreateOptionsSerializer(instance=product,
                                                           context=serializer_context).to_representation(product))

    @action(methods=['GET'], detail=True)
    def edit_options(self, request, pk):
        del pk  # unused
        order_item = self.get_object()
        order_item_cycle_id = request.query_params.get('cycle')
        product = order_item.product
        cart = self.cart
        if not product:
            return Response({'detail': 'Specify a product code or id'})
        elif product.price_model == PricingModel.free:
            serializer_context = {'cycle': None, 'cart': cart}
            result = CartProductCreateOptionsSerializer(instance=product,
                                                        context=serializer_context).to_representation(product)
            return Response(result)
        elif order_item_cycle_id:
            try:
                order_item_cycle = product.cycles.available_for_order(
                    currency=cart.currency
                ).get(id=order_item_cycle_id)
            except (ProductCycle.DoesNotExist, ProductCycle.MultipleObjectsReturned, TypeError, ValueError):
                raise serializers.ValidationError({'detail': 'Product cycle is not available'})
        else:
            order_item_cycle = order_item.cycle

        #  NOTE(tomo): order_item.cycle is a different model than Product.cycle
        product_cycles_available = product.cycles.available_for_order(currency=cart.currency)
        try:
            product_cycle = product_cycles_available.filter(cycle=order_item_cycle.cycle,
                                                            cycle_multiplier=order_item_cycle.cycle_multiplier,
                                                            currency=order_item_cycle.currency).get()
        except (ProductCycle.DoesNotExist, ProductCycle.MultipleObjectsReturned, TypeError, ValueError):
            raise serializers.ValidationError({'detail': 'Product cycle is not available'})
        serializer_context = {'cycle': product_cycle, 'cart': cart}
        result = CartProductCreateOptionsSerializer(instance=product,
                                                    context=serializer_context).to_representation(product)
        return Response(result)
