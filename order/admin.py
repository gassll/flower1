from django.contrib import admin

from catalog.models import Category
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price", "is_available")
    search_fields = ("name", "description", "category__name")
    list_filter = ("category", "is_available")
    ordering = ("name",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")