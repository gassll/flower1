from django.db import models
from django.conf import settings


class Order(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Наличные'),
        ('card', 'Банковская карта'),
    ]

    DELIVERY_TIMES = [
        ('09:00-11:00', '09:00 - 11:00'),
        ('11:00-13:00', '11:00 - 13:00'),
        ('13:00-15:00', '13:00 - 15:00'),
        ('15:00-17:00', '15:00 - 17:00'),
        ('17:00-19:00', '17:00 - 19:00'),
        ('19:00-21:00', '19:00 - 21:00'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )

    name = models.CharField(max_length=200, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.TextField(verbose_name='Адрес доставки', null=True, blank=True)
    delivery_date = models.DateField(verbose_name='Дата доставки', null=True, blank=True)
    delivery_time = models.CharField(
        max_length=50,
        choices=DELIVERY_TIMES,
        verbose_name='Время доставки',
        null=True,
        blank=True
    )

    comment = models.TextField(blank=True, verbose_name='Комментарий')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, verbose_name='Способ оплаты')

    cart_items = models.JSONField(default=list, verbose_name='Товары в заказе')

    total_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Сумма заказа')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', null=True)

    def __str__(self):
        return f'Заказ #{self.id}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']