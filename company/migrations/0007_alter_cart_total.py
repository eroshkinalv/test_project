# Generated by Django 5.1.7 on 2025-04-12 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("company", "0006_alter_orderitem_order_item"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="total",
            field=models.IntegerField(blank=True, null=True, verbose_name="Сумма заказа"),
        ),
    ]
