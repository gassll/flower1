from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "name",
        "phone",
        "products_list",
        "total_sum",
        "created_at",
    )

    readonly_fields = ("total_sum", "created_at", "pretty_cart_items")

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
        ("Товары", {
            "fields": ("pretty_cart_items",)
        }),
        ("Системная информация", {
            "fields": ("created_at",),
            "classes": ("collapse",)
        }),
    )

    def products_list(self, obj):
        if not obj.cart_items:
            return "—"

        return ", ".join(
            f"{item.get('product_name')} x{item.get('quantity')}"
            for item in obj.cart_items
        )

    products_list.short_description = "Товары"

    def pretty_cart_items(self, obj):
        if not obj.cart_items:
            return "—"

        return "\n".join(
            f"🛒 {item.get('product_name')} — {item.get('quantity')} шт. — {item.get('product_price')} ₽"
            for item in obj.cart_items
        )

    pretty_cart_items.short_description = "Товары"