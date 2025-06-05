from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from company.models import Company
from company.serializers import CompanySerializer
from finance.models import Payment, ItemPrice, OrderItem, Cart
from users.serializers import UserSerializer


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class ItemPriceSerializer(ModelSerializer):

    class Meta:
        model = ItemPrice
        fields = "__all__"


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
