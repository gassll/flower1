from django.contrib import admin
from .models import Order, OrderStructure


# Inline для отображения товаров в заказе
class OrderStructureInline(admin.TabularInline):
    model = OrderStructure
    extra = 1  # пустая строка для добавления нового товара
    fields = ['product', 'quantity', 'unit_price']  # какие поля показывать
    readonly_fields = ['unit_price']  # цена только для чтения
    autocomplete_fields = ['product']  # поиск товара с автодополнением
    verbose_name = "Товар"
    verbose_name_plural = "Товары в заказе"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "phone", "delivery_date", "payment_method", "total_sum", "created_at")
    list_filter = ("payment_method", "delivery_date", "created_at")
    search_fields = ("name", "phone", "address", "id")
    readonly_fields = ("total_sum", "created_at")

    # Подключаем inline для отображения товаров
    inlines = [OrderStructureInline]

    # Опционально: группировка полей
    fieldsets = (
        ("Информация о заказе", {
            "fields": ("user", "name", "phone", "address")
        }),
        ("Доставка", {
            "fields": ("delivery_date", "delivery_time", "comment")
        }),
        ("Оплата", {
            "fields": ("payment_method", "total_sum")
        }),
        ("Системная информация", {
            "fields": ("created_at", "cart_items"),
            "classes": ("collapse",)
        })
    )


@admin.register(OrderStructure)
class OrderStructureAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "unit_price")
    list_filter = ("order",)
    search_fields = ("order__id", "product__name")