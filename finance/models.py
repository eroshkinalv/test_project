from django.db import models

from company.models import Item, Company
from users.models import User


class ItemPrice(models.Model):
    """Модель цены на товар"""

    owner = models.ForeignKey("users.User", verbose_name="Пользователь", on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="Изделие", blank=True, null=True)
    price_per_item = models.PositiveIntegerField(verbose_name="Цена за единцу товара")
    quantity_available = models.PositiveIntegerField(default=0, verbose_name="Количество изделий на складе")


    class Meta:
        verbose_name = "Цена"
        verbose_name_plural = "Цены"


class OrderItem(models.Model):
    """Модель заказа товаров"""

    owner = models.ForeignKey("users.User", verbose_name="Пользователь", on_delete=models.CASCADE, blank=True, null=True)
    order_item = models.ForeignKey(Item, verbose_name="Изделие", on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1, verbose_name="Количество")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        verbose_name = "Заказанный товары"
        verbose_name_plural = "Заказанные товары"


class Cart(models.Model):
    """Модель корзины заказов"""

    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name="Заказчик", blank=True, null=True)
    order_items = models.ManyToManyField(OrderItem, verbose_name="Заказанные издения", related_name="order_items")
    ordered = models.BooleanField(default=False)
    total = models.IntegerField(verbose_name="Сумма заказа", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


class Payment(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    company = models.ForeignKey(
        Company, verbose_name="Баланс по счету", on_delete=models.SET_NULL, null=True, blank=True
    )

    quantity = models.PositiveIntegerField(verbose_name="Количество товара", null=True, blank=True)

    payment_amount = models.PositiveIntegerField(default=0, verbose_name="Сумма оплаты")

    METHOD_CHOICES = (("Наличные", "Наличные"), ("Перевод на счет", "Перевод на счет"))
    payment_method = models.CharField(max_length=250, verbose_name="Способ оплаты", choices=METHOD_CHOICES)

    session_id = models.CharField(max_length=250, verbose_name="id сессии платежа", null=True, blank=True)
    payment_link = models.URLField(max_length=400, verbose_name="Ссылка на оплату", null=True, blank=True)
    status = models.CharField(
        max_length=250,
        verbose_name="Статус платежа",
        null=True,
        blank=True,
        help_text="complete(оплачен)/expired(не действителен)/open(ожидает оплаты)",
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __int__(self):
        return self.payment_amount
