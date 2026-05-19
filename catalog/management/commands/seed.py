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

        # -----------------------------
        # Очищаем базу
        # -----------------------------
        self.stdout.write('Очищаем базу данных...')

        Product.objects.all().delete()
        Category.objects.all().delete()

        # -----------------------------
        # Очищаем media
        # -----------------------------
        self.clear_media_folder()

        # -----------------------------
        # Получаем изображения
        # -----------------------------
        product_images = self.get_images_from_folder('images')
        icon_images = self.get_images_from_folder('icons')

        self.stdout.write(f'Найдено изображений товаров: {len(product_images)}')
        self.stdout.write(f'Найдено иконок: {len(icon_images)}')

        # -----------------------------
        # Категории
        # -----------------------------
        category_names = [
            'Розы',
            'Тюльпаны',
            'Пионы',
            'Хризантемы',
            'Лилии',
            'Орхидеи',
            'Свадебные букеты',
            'Композиции в корзинах',
            'Цветы в горшках',
            'Сухоцветы',
            'Вазы',
            'Корзины цветов',
            'Авторские букеты'
        ]

        categories = []

        for name in category_names:
            category = Category.objects.create(name=name)

            # Добавляем иконку
            if icon_images:
                random_icon = random.choice(icon_images)
                self.add_image_to_object(category, random_icon, 'icons')

            categories.append(category)

            self.stdout.write(f'✓ Создана категория: {name}')

        # -----------------------------
        # Описания
        # -----------------------------
        descriptions = [
            'Изысканный букет из свежих цветов',
            'Нежная композиция ручной работы',
            'Авторский букет от флориста',
            'Свежие цветы с доставкой',
            'Роскошная композиция для особого случая',
            'Стильный букет в современном оформлении',
            'Элегантная композиция в пастельных оттенках',
            'Премиальный букет из отборных цветов'
        ]

        # -----------------------------
        # Товары по категориям
        # -----------------------------
        products_by_category = {
            'Вазы': [
                'Ваза v.125',
                'Ваза v.116',
                'Ваза v.124',
                'Ваза v.120',
                'Ваза v.106'
            ],

            'Корзины цветов': [
                'Корзина "PINK PUNK"',
                'Корзина ароматной сирени',
                'Корзина "Лимонад с ревенем"',
                'Корзина ромашек'
            ],

            'Пионы': [
                'Нежность пионов',
                'Розовое облако',
                'Нежный рассвет'
            ],

            'Авторские букеты': [
                'Авторский букет "Мираж"',
                'Авторский букет "Летняя прохлада"',
                'Садовый букет "Лимонад с ревенем"'
            ],

            'Лилии': [
                'Белая лилия',
                'Царская лилия',
                'Лунный свет'
            ],

            'Орхидеи': [
                'Экзотическая орхидея',
                'Тропическая мечта'
            ],

            'Свадебные букеты': [
                'Букет невесты',
                'Свадебная гармония'
            ],

            'Композиции в корзинах': [
                'Корзина счастья',
                'Цветочная симфония',
                'Праздничная корзина'
            ],

            'Цветы в горшках': [
                'Домашняя орхидея',
                'Зеленый уют'
            ],

            'Сухоцветы': [
                'Лавандовое настроение',
                'Прованс',
                'Сиреневое облако'
            ]
        }

        # -----------------------------
        # Создаем товары
        # -----------------------------
        self.stdout.write('\nСоздаем товары...')

        products_created = 0

        for category_name, product_list in products_by_category.items():

            category = Category.objects.get(name=category_name)

            for product_name in product_list:

                price = random.randint(1000, 15000)
                price = round(price / 50) * 50

                product = Product.objects.create(
                    category=category,
                    name=product_name,
                    description=(
                            random.choice(descriptions)
                            + '. '
                            + fake.text(max_nb_chars=120)
                    ),
                    price=price,
                    is_available=random.choice([True, True, True, False]),
                    is_recommended=random.choice([True, False])
                )

                # Добавляем изображение
                if product_images:
                    random_image = random.choice(product_images)
                    self.add_image_to_object(product, random_image, 'images')

                products_created += 1

                self.stdout.write(f'   ✓ {product_name}')

        # -----------------------------
        # Итог
        # -----------------------------
        self.stdout.write(
            self.style.SUCCESS('\n✓ База данных успешно заполнена!')
        )

        self.stdout.write(
            self.style.SUCCESS(f'✓ Категорий: {len(categories)}')
        )

        self.stdout.write(
            self.style.SUCCESS(f'✓ Товаров: {products_created}')
        )

    # =========================================================
    # Получение изображений
    # =========================================================
    def get_images_from_folder(self, subfolder):

        images = []

        seed_dir = os.path.join(
            settings.BASE_DIR,
            'media_seed',
            subfolder
        )

        if os.path.exists(seed_dir):

            for file in os.listdir(seed_dir):

                if file.lower().endswith(
                        ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg')
                ):
                    images.append(file)

            self.stdout.write(
                f'   Найдено {len(images)} файлов в {subfolder}'
            )

        else:
            self.stdout.write(
                self.style.WARNING(f'Папка не найдена: {seed_dir}')
            )

        return images

    # =========================================================
    # Добавление изображения
    # =========================================================
    def add_image_to_object(self, obj, image_filename, subfolder='images'):

        source_path = os.path.join(
            settings.BASE_DIR,
            'media_seed',
            subfolder,
            image_filename
        )

        if os.path.exists(source_path):

            try:
                extension = os.path.splitext(image_filename)[1]

                unique_filename = (
                    f"{slugify(obj.name)}_"
                    f"{random.randint(1000, 9999)}"
                    f"{extension}"
                )

                with open(source_path, 'rb') as f:

                    django_file = File(f, name=unique_filename)

                    obj.image.save(
                        unique_filename,
                        django_file,
                        save=True
                    )

                return True

            except Exception as e:

                self.stdout.write(
                    self.style.WARNING(
                        f'Ошибка загрузки {image_filename}: {e}'
                    )
                )

        return False

    # =========================================================
    # Очистка media
    # =========================================================
    def clear_media_folder(self):

        media_path = os.path.join(settings.BASE_DIR, 'media')

        if os.path.exists(media_path):

            try:
                shutil.rmtree(media_path)
                self.stdout.write('✓ Папка media очищена')

            except Exception as e:

                self.stdout.write(
                    self.style.WARNING(
                        f'Не удалось очистить media: {e}'
                    )
                )

        os.makedirs(media_path, exist_ok=True)


