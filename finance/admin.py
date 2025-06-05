from django.contrib import admin

from finance.models import OrderItem, Cart, ItemPrice, Payment


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order_item", "quantity")
    search_fields = ("order_item",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "total")
    search_fields = ("owner",)


@admin.register(ItemPrice)
class ItemPriceAdmin(admin.ModelAdmin):
    list_display = ("id", "owner",)
    search_fields = ("owner",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    search_fields = ("user",)
