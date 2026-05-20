from django.db import models
from slugify import slugify
from autoslug import AutoSlugField
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name='Изображение')
    is_recommended = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user} - {self.product}'


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user} - {self.product}'


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

    # Используйте settings.AUTH_USER_MODEL вместо User
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             verbose_name='Пользователь')
    name = models.CharField(max_length=200, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.TextField(verbose_name='Адрес доставки')
    delivery_date = models.DateField(verbose_name='Дата доставки')
    delivery_time = models.CharField(max_length=50, choices=DELIVERY_TIMES, verbose_name='Время доставки')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, verbose_name='Способ оплаты')
    cart_items = models.JSONField(default=dict, verbose_name='Товары в заказе')
    total_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Сумма заказа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.CharField(max_length=20, default='new', verbose_name='Статус заказа')

    def __str__(self):
        return f'Заказ #{self.id} от {self.created_at.strftime("%d.%m.%Y")}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']