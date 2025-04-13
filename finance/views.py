from rest_framework.viewsets import ModelViewSet

from company.models import Company
from finance.models import Payment, OrderItem, ItemPrice, Cart

from finance.serializers import PaymentSerializer, OrderItemSerializer, CartSerializer, ItemPriceSerializer
from finance.services import create_stripe_product, create_stripe_price, create_stripe_session, create_stripe_checkout
from users.permissions import IsOwner
from decimal import *


class PaymentViewSet(ModelViewSet):

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filterset_fields = ["date", "payment_amount", "payment_method", "cart"]

    def perform_create(self, serializer):

        user_payment = serializer.save(user=self.request.user)

        company_balance = float(user_payment.company.balance)
        print(company_balance)
        payment_amount = 0
        if company_balance < 0:
            payment_amount = abs(company_balance)
            print(payment_amount)

        user_payment.payment_amount = payment_amount
        product = create_stripe_product(user_payment.company)
        amount = create_stripe_price(user_payment.payment_amount, product)
        session_id, payment_link = create_stripe_session(amount)
        user_payment.session_id = session_id
        user_payment.payment_link = payment_link
        checkout = create_stripe_checkout(session_id)
        user_payment.status = checkout.status
        user_payment.save()


class OrderItemViewSet(ModelViewSet):

    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = (IsOwner,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CartViewSet(ModelViewSet):

    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (IsOwner,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

        cart =serializer.save()
        company = Company.objects.filter(owner=self.request.user).first()
        company_owner = company.supplier.owner
        cart_items = cart.order_items.all()

        total = 0

        for item in cart_items:
            i = OrderItem.objects.filter(id=item.id).first().order_item
            price_per_item = ItemPrice.objects.filter(item=i, owner=company_owner.id).first().price_per_item
            quantity = OrderItem.objects.filter(id=item.id).first().quantity

            price = float(price_per_item * quantity)

            total += price

        cart.total = total
        cart.ordered = True
        cart.save()

        if cart.ordered:
            getcontext().prec = 2
            company.balance -= Decimal(cart.total)
            company.save()


class ItemPriceViewSet(ModelViewSet):

    queryset = ItemPrice.objects.all()
    serializer_class = ItemPriceSerializer
    permission_classes = (IsOwner,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
