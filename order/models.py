from django.db import models

from catalog.models import Product


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    # customer_id = models.ForeignKey()
    order_date = models.DateField()
    delivery_date = models.DateField(null=True, blank=True)
    delivery_address = models.TextField(null=True, blank=True)
    # status_id = models.ForeignKey()
    total_amount = models.DecimalField(max_digits=10,
        decimal_places=2)

class Status(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class OrderStructure(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField( max_digits=10,
        decimal_places=2,)