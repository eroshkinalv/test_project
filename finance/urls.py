from rest_framework.routers import SimpleRouter


from finance.views import OrderItemViewSet, CartViewSet, ItemPriceViewSet, PaymentViewSet
from users.apps import UsersConfig


app_name = UsersConfig.name

router = SimpleRouter()

router.register(r"payment", PaymentViewSet, basename="payment")
router.register(r"order_item", OrderItemViewSet, basename="order_item")
router.register(r"cart", CartViewSet, basename="cart")
router.register(r"item_price", ItemPriceViewSet, basename="item_price")

urlpatterns = []

urlpatterns += router.urls
