import os
import random
import shutil

from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from django.utils.text import slugify

from faker import Faker

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Stable production seed (safe + deterministic image mapping)"

    DATA = {
        "Вазы": [
            ("Ваза v.120", "vases/vase1.jpg"),
            ("Ваза v.101", "vases/vase2.jpg"),
            ("Ваза v.106", "vases/vase3.webp"),
            ("Ваза v.120", "vases/vase4.jpg"),
            ("Ваза v.122", "vases/vase5.jpg"),
            ("Ваза v.125", "vases/vase6.webp"),
        ],

        "Корзины цветов": [
            ("Корзина ароматной сирени", "baskets/baskets1.webp"),
            ("Корзина PINK PUNK", "baskets/baskets2.webp"),
            ("Корзина Лимонад с ревенем", "baskets/baskets3.webp"),
        ],

        "Цветы в коробке": [
            ("Шляпная коробка «Лимончелло»", "boxes/box1.webp"),
            ("Шляпная коробка «Монпансье»", "boxes/box2.webp"),
            ("Шляпная коробка «Нежные чувства»", "boxes/box3.jpg"),
            ("Шляпная коробка «Розовая матча»", "boxes/box4.webp"),
        ],

        "Авторские букеты": [
            ("Авторский букет «Летняя прохлада»", "bouquets/bouquets1.webp"),
            ("Садовый  букет «Лимонад с ревенем»", "bouquets/bouquets2.webp"),
            ("Садовый букет «Мохито»", "bouquets/bouquets3.webp"),
            ("Авторский букет «Кьянти»", "bouquets/bouquets4.webp"),
            ("Авторский букет «Арбузный смузи»", "bouquets/bouquets5.webp"),
        ],

        "Моно дуо трио букеты": [
            ("Пионовидные розы «Джентл Трендсеттер»", "mono_duo_trio/mono_duo_trio1.webp"),
            ("Трио-букет «Новая Антуанетта»", "mono_duo_trio/mono_duo_trio2.webp"),
            ("Белая кустовая маттиола", "mono_duo_trio/mono_duo_trio3.webp"),
            ("Дуо-букет «Мандарин и оксипеталум»", "mono_duo_trio/mono_duo_trio4.webp"),
        ],

        "Свадебные букеты": [
            ("Букет невесты LOV 73", "wedding/wed1.webp"),
            ("Букет невесты LOV 98", "wedding/wed2.webp"),
            ("Букет невесты LOV 85", "wedding/wed3.webp"),
        ],
    }


    def handle(self, *args, **kwargs):
        self.fake = Faker("ru_RU")

        self.reset()
        self.create_categories()
        self.create_products()

        self.stdout.write(self.style.SUCCESS("✅ SEED DONE"))

    def reset(self):
        self.stdout.write("🧹 Reset...")

        Product.objects.all().delete()
        Category.objects.all().delete()

        media_path = os.path.join(settings.BASE_DIR, "media")
        if os.path.exists(media_path):
            shutil.rmtree(media_path)

        os.makedirs(media_path, exist_ok=True)


    def create_categories(self):
        self.stdout.write("🌸 Creating categories...")

        self.categories = {}

        for name in self.DATA.keys():
            obj, _ = Category.objects.get_or_create(
                name=name,
                defaults={"slug": slugify(name)}
            )

            self.categories[name] = obj
            self.stdout.write(f"✔ {name}")


    def create_products(self):
        self.stdout.write("🌷 Creating products...")

        for category_name, products in self.DATA.items():

            category = self.categories[category_name]

            for product_name, image_path in products:

                product = Product.objects.create(
                    category=category,
                    name=product_name,
                    description=self.fake.text(120),
                    price=self.random_price(),
                    is_available=True,
                    is_recommended=False,
                )

                self.attach_image(product, image_path)

                self.stdout.write(f"   ✓ {product_name}")


    def attach_image(self, obj, relative_path):

        full_path = os.path.join(
            settings.BASE_DIR,
            "media_seed",
            relative_path
        )

        if not os.path.exists(full_path):
            self.stdout.write(f"⚠ missing image: {relative_path}")
            return

        try:
            with open(full_path, "rb") as f:
                obj.image.save(
                    self.unique_name(full_path),
                    File(f),
                    save=True
                )
        except Exception as e:
            self.stdout.write(f"⚠ image error: {e}")


    def unique_name(self, path):
        import uuid
        return f"{uuid.uuid4().hex}_{os.path.basename(path)}"

    def random_price(self):
        return round(random.randint(1000, 20000) / 50) * 50