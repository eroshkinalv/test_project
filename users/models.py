from django.contrib.auth.models import AbstractUser
from django.db import models

from company.models import Item


class User(AbstractUser):

    username = None

    first_name = models.CharField(verbose_name="Имя", max_length=150, blank=True)
    last_name = models.CharField(verbose_name="Фамилия", max_length=150, blank=True)

    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=120, null=True, blank=True, verbose_name='Телефон')
    image = models.ImageField(upload_to='profile_img/', default='/profile_img/ava_001.png',
                              null=True, blank=True, verbose_name='Аватар')
    country = models.CharField(max_length=120, null=True, blank=True, verbose_name='Страна')

    STATUS_CHOICES = (('Менеджер', 'Менеджер'), ('Пользователь', 'Пользователь'))
    status = models.CharField(max_length=250, verbose_name='Статус', choices=STATUS_CHOICES, null=True, blank=True)

    is_blocked = models.BooleanField(default=False, verbose_name='Блокировка пользователя')

    is_active = models.BooleanField(default=True, verbose_name='Блокировка пользователя')

    token = models.CharField(max_length=100, verbose_name='Токен', null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        # permissions = [
        #     ("managers", "Can view and block users"),
        # ]

    def __str__(self):
        return self.email


class Payment(models.Model):

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    item = models.ForeignKey(
        Item, verbose_name="Оплаченный товар", on_delete=models.SET_NULL, null=True, blank=True
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
