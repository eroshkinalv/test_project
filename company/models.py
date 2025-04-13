import datetime

from django.db import models


class Item(models.Model):

    """Модель изделия"""

    name = models.CharField(max_length=200, verbose_name="Изделие", help_text="Название производимой продукции")
    mark = models.CharField(max_length=200, verbose_name="Модель", help_text="Название модели изделия")
    release_date = models.DateField(default=datetime.date.today(), max_length=200, verbose_name="Дата выпуска")
    owner = models.ForeignKey("users.User", verbose_name="Пользователь", on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "Изделие"
        verbose_name_plural = "Изделия"
        ordering = ("name",)

    def __str__(self):
        return f"{self.name} {self.mark}"


class Company(models.Model):

    """Модель компании"""

    owner = models.ForeignKey("users.User", verbose_name="Пользователь", on_delete=models.CASCADE, blank=True, null=True)

    COMPANY_TYPES = (
        ('Завод', 'Завод'),
        ('Розничная сеть', 'Розничная сеть'),
        ('Индивидуальный предприниматель', 'Индивидуальный предприниматель'),
    )

    company_type = models.CharField(max_length=200, verbose_name="Поставщик", help_text="Название поставщика", choices=COMPANY_TYPES)

    name = models.CharField(max_length=200, verbose_name="Фирма", help_text="Название фирмы")
    email = models.EmailField(max_length=200, verbose_name="Email", help_text="Адрес электронной почты")
    country = models.CharField(max_length=200, verbose_name="Страна")
    city = models.CharField(max_length=200, verbose_name="Город")
    street = models.CharField(max_length=200, verbose_name="Улица")
    house = models.CharField(max_length=200, verbose_name="Номер дома")

    supplier = models.ForeignKey("self", verbose_name="Поставщик", on_delete=models.SET_NULL, help_text="Название поставщика", blank=True, null=True, related_name="item_supplier")

    item = models.ManyToManyField(Item, verbose_name="Изделия", related_name="items", blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    balance = models.IntegerField(verbose_name="Задолженность", default=0)

    class Meta:
        verbose_name = "Фирма"
        verbose_name_plural = "Фирмы"
        ordering = ("name",)
