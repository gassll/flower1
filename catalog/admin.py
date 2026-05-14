from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image_preview', 'is_featured', 'description']
    search_fields = ['name']
    list_filter = ['is_featured']
    list_editable = ['is_featured']

    fields = ['name', 'slug', 'description', 'image', 'image_preview', 'is_featured']
    readonly_fields = ['slug', 'image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 5px;" />',
                obj.image.url
            )
        return "Нет изображения"

    image_preview.short_description = 'Превью'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'is_recommended', 'image_preview']
    list_filter = ['category', 'is_available', 'is_recommended']
    search_fields = ['name']
    list_editable = ['price', 'is_available', 'is_recommended']

    fields = ['name', 'category', 'price', 'description', 'image', 'image_preview', 'is_available', 'is_recommended']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 5px;" />',
                obj.image.url
            )
        return "Нет изображения"

    image_preview.short_description = 'Превью'