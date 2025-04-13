from rest_framework.viewsets import ModelViewSet

from company.models import Company
from finance.models import Payment, OrderItem, ItemPrice, Cart, BalanceSheet

from finance.serializers import PaymentSerializer, OrderItemSerializer, CartSerializer, ItemPriceSerializer
from finance.services import create_stripe_product, create_stripe_price, create_stripe_session, create_stripe_checkout
from users.permissions import IsOwner


class PaymentViewSet(ModelViewSet):

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filterset_fields = ["date", "payment_amount", "payment_method", "cart"]

    def perform_create(self, serializer):

        user_payment = serializer.save(user=self.request.user)
        payment_id = user_payment.cart.id
        payment_amount = Cart.objects.filter(id=payment_id).first().total

        user_payment.payment_amount = payment_amount

        product = create_stripe_product(user_payment.cart)
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


class ItemPriceViewSet(ModelViewSet):

    queryset = ItemPrice.objects.all()
    serializer_class = ItemPriceSerializer
    permission_classes = (IsOwner,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BalanceViewSet(ModelViewSet):

    queryset = BalanceSheet.objects.all()
    serializer_class = ItemPriceSerializer
    permission_classes = (IsOwner,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

        balance = serializer.save()

        cart = Cart.objects.filter(owner=self.request.user).first()
        balance.balance -= cart.total
        balance.save()
