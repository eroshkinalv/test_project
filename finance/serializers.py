from rest_framework.serializers import ModelSerializer

from finance.models import Payment, ItemPrice, OrderItem, Cart, BalanceSheet


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class ItemPriceSerializer(ModelSerializer):

    class Meta:
        model = ItemPrice
        exclude = ("owner",)


class OrderItemSerializer(ModelSerializer):

    class Meta:
        model = OrderItem
        fields = "__all__"
        read_only_fields = ["owner", "created_at"]


class CartSerializer(ModelSerializer):

    class Meta:
        model = Cart
        fields = "__all__"
        read_only_fields = ["owner", "total", "created_at"]


class BalanceSerializer(ModelSerializer):

    class Meta:
        model = BalanceSheet
        fields = "__all__"
        read_only_fields = ["owner", "updated_at", "created_at"]