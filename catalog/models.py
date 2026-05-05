from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    is_available = models.BooleanField(default=True)


