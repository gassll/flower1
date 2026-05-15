from django.contrib import admin
from django.db import models
from image_uploader_widget.widgets import ImageUploaderWidget
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_featured']
    search_fields = ['name']
    list_filter = ['is_featured']
    list_editable = ['is_featured']

    # ГЛАВНОЕ: переопределяем виджет для ImageField
    formfield_overrides = {
        models.ImageField: {'widget': ImageUploaderWidget},
    }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'is_recommended']
    list_filter = ['category', 'is_available', 'is_recommended']
    search_fields = ['name']
    list_editable = ['price', 'is_available', 'is_recommended']

    # ГЛАВНОЕ: переопределяем виджет для ImageField
    formfield_overrides = {
        models.ImageField: {'widget': ImageUploaderWidget},
    }