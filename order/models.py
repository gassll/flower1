from django.contrib.auth.models import User
from django.db import models

from catalog.models import Product
from django.conf import settings


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    # customer = models.ForeignKey()
    order_date = models.DateField()
    delivery_date = models.DateField(null=True, blank=True)
    delivery_address = models.TextField(null=True, blank=True)
    # status = models.ForeignKey()
    total_amount = models.DecimalField(max_digits=10,
        decimal_places=2)

    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('process','В обработке'),
        ('done','Завершена'),
    ]

    PAYMENT_CHOICES = [
        ('cash','наличные'),
        ('card','Карта'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=200)
    start_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return f'{self.course_name} - {self.user.username}'

class Status(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


class OrderStructure(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items',null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', null=True, blank=True)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

