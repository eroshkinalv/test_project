from django.db import models


class Item(models.Model):

    """Модель изделия"""

    name = models.CharField(max_length=200, verbose_name="Изделие", help_text="Название производимой продукции")
    mark = models.CharField(max_length=200, verbose_name="Модель", help_text="Название модели изделия")
    release_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Изделие"
        verbose_name_plural = "Изделия"
        ordering = ("name",)

    def __str__(self):
        return f"{self.name} {self.mark}"


class Company(models.Model):

    """Модель компании"""

    COMPANY_TYPES = (
        ('Завод', 'Завод'),
        ('Розничная сеть', 'Розничная сеть'),
        ('Индивидуальный предприниматель', 'Индивидуальный предприниматель'),
    )

    company = models.CharField(max_length=200, verbose_name="Производство", help_text="Название места производства", choices=COMPANY_TYPES)

    name = models.CharField(max_length=200, verbose_name="Фирма", help_text="Название фирмы")
    email = models.CharField(max_length=200, verbose_name="Email", help_text="Адрес электронной почты")
    country = models.CharField(max_length=200, verbose_name="Страна")
    city = models.CharField(max_length=200, verbose_name="Город")
    street = models.CharField(max_length=200, verbose_name="Улица")
    house = models.CharField(max_length=200, verbose_name="Номер дома")

    item = models.ManyToManyField(Item, verbose_name="Изделия", related_name="items")

    supplier = models.ForeignKey("self", verbose_name="Поставщик", on_delete=models.SET_NULL, help_text="Название поставщика", blank=True, null=True, related_name="item_supplier")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    debt = models.IntegerField(verbose_name="Задолженность")

    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Фирма"
        verbose_name_plural = "Фирмы"
        ordering = ("name",)

    def __str__(self):
        return {self.name}


class OrderItem(models.Model):
    """Модель заказа товаров"""

    order_item = models.ForeignKey(Item, verbose_name="Изделие", on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1, verbose_name="Количество")


class Cart(models.Model):
    """Модель корзины заказов"""

    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name="Заказчик")
    order_items = models.ManyToManyField(OrderItem, verbose_name="Заказанные издения", related_name="order_items")
    ordered = models.BooleanField(default=False)
    total = models.IntegerField(verbose_name="Сумма заказа")
