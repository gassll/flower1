# catalog/management/commands/fill_db.py
import random
import os
import shutil
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from django.utils.text import slugify
from faker import Faker

from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Заполнение базы данных цветочного магазина тестовыми данными'

    def handle(self, *args, **kwargs):
        fake = Faker('ru_RU')

        # Очищаем базу
        self.stdout.write('Очищаем базу данных...')
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Очищаем медиа папку
        self.clear_media_folder()

        # Получаем все изображения из папок
        product_images = self.get_images_from_folder('images')
        icon_images = self.get_images_from_folder('icons')

        self.stdout.write(f'Найдено изображений товаров: {len(product_images)}')
        self.stdout.write(f'Найдено иконок: {len(icon_images)}')

        # Создаем категории
        category_names = [
            'Розы', 'Тюльпаны', 'Пионы', 'Хризантемы', 'Лилии',
            'Орхидеи', 'Свадебные букеты', 'Композиции в корзинах',
            'Цветы в горшках', 'Сухоцветы'
        ]

        categories = []
        for name in category_names:
            category = Category(name=name)
            category.save()

            # Для категорий используем иконки (если есть)
            if icon_images:
                random_icon = random.choice(icon_images)
                self.add_image_to_object(category, random_icon, 'icons')
            elif product_images:
                # Если иконок нет, используем обычные изображения
                random_image = random.choice(product_images)
                self.add_image_to_object(category, random_image, 'images')

            categories.append(category)
            self.stdout.write(f'Создана категория: {name}')

        # Названия товаров
        product_names = [
            'Классический букет роз', 'Нежность пионов', 'Солнечные тюльпаны',
            'Белая лилия', 'Весеннее настроение', 'Алая страсть', 'Невеста',
            'Цветочная симфония', 'Розовое облако', 'Сиреневый рай',
            'Осенний вальс', 'Зимняя сказка', 'Экзотическая орхидея',
            'Полевые цветы', 'Корзина счастья', 'Лавандовое настроение',
            'Букет невесты', 'Дыхание весны', 'Царская лилия', 'Премиум букет',
            'Минимализм', 'Яркий акцент', 'Нежный рассвет', 'Вечерняя романтика',
            'Прованс', 'Розовая мечта', 'Сиреневое облако', 'Золотая осень',
            'Белоснежная чистота', 'Королевский букет'
        ]

        # Описания
        descriptions = [
            'Изысканный букет из свежих цветов, собранный вручную нашими флористами',
            'Нежные цветы в элегантной упаковке, подарят радость и хорошее настроение',
            'Шикарная композиция для особого случая или просто так',
            'Свежайшие цветы с доставкой по городу',
            'Эффектный букет, который точно запомнится',
            'Стильная композиция в современном стиле',
            'Классический букет для любимых и близких',
            'Роскошная композиция с дополнительным декором',
            'Букет с доставкой день в день',
            'Авторская работа наших флористов',
            'Эксклюзивный букет от ведущих флористов',
            'Невероятно красивая композиция для особого дня'
        ]

        # Создаем товары
        self.stdout.write('\nСоздаем товары...')
        products_created = 0

        for i in range(50):  # Создаем 50 товаров
            price = random.randint(500, 15000)
            price = round(price / 50) * 50

            name = random.choice(product_names)
            if Product.objects.filter(name=name).exists():
                name = f"{name} {i + 1}"

            product = Product(
                category=random.choice(categories),
                name=name,
                description=random.choice(descriptions) + '. ' + fake.text(max_nb_chars=150),
                price=price,
                is_available=random.choice([True, True, True, True, False]),
                is_recommended=random.choice([True, False])
            )
            product.save()

            # Для товаров используем изображения из папки images
            if product_images:
                random_image = random.choice(product_images)
                self.add_image_to_object(product, random_image, 'images')

            products_created += 1

            if products_created % 10 == 0:
                self.stdout.write(f'   Создано товаров: {products_created}')

        self.stdout.write(self.style.SUCCESS(f'\n✓ База данных успешно заполнена!'))
        self.stdout.write(self.style.SUCCESS(f'✓ Категорий: {len(categories)}'))
        self.stdout.write(self.style.SUCCESS(f'✓ Товаров: {products_created}'))
        self.stdout.write(
            self.style.SUCCESS(f'✓ Использовано изображений товаров: {min(len(product_images), products_created)}'))
        self.stdout.write(self.style.SUCCESS(f'✓ Использовано иконок: {min(len(icon_images), len(categories))}'))

    def get_images_from_folder(self, subfolder):
        """Получает список всех изображений из указанной подпапки media_seed"""
        images = []
        seed_dir = os.path.join(settings.BASE_DIR, 'media_seed', subfolder)

        if os.path.exists(seed_dir):
            for file in os.listdir(seed_dir):
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg')):
                    images.append(file)
            self.stdout.write(f'   Найдено {len(images)} файлов в {subfolder}')
        else:
            self.stdout.write(self.style.WARNING(f'   Папка не найдена: {seed_dir}'))

        return images

    def add_image_to_object(self, obj, image_filename, subfolder='images'):
        """Добавляет изображение к объекту модели"""
        source_path = os.path.join(settings.BASE_DIR, 'media_seed', subfolder, image_filename)

        if os.path.exists(source_path):
            try:
                # Генерируем уникальное имя файла
                extension = os.path.splitext(image_filename)[1]
                unique_filename = f"{slugify(obj.name)}_{random.randint(1000, 9999)}{extension}"

                with open(source_path, 'rb') as f:
                    django_file = File(f, name=unique_filename)
                    obj.image.save(unique_filename, django_file, save=True)
                self.stdout.write(f'     ✓ Загружено: {image_filename} -> {obj.name}')
                return True
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'     ✗ Ошибка загрузки {image_filename}: {e}'))
        else:
            self.stdout.write(self.style.WARNING(f'     ✗ Файл не найден: {source_path}'))

        return False

    def clear_media_folder(self):
        media_path = os.path.join(settings.BASE_DIR, 'media')
        if os.path.exists(media_path):
            try:
                shutil.rmtree(media_path)
                self.stdout.write('Папка media очищена')
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Не удалось очистить media: {e}'))

        # Создаем папку media заново
        os.makedirs(media_path, exist_ok=True)
