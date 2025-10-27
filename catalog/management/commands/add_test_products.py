# catalog/management/commands/add_test_products.py
from django.core.management.base import BaseCommand
from catalog.models import Category, Product
import random


class Command(BaseCommand):
    help = 'Добавляет тестовые категории и продукты в базу данных'

    def handle(self, *args, **kwargs):
        # Очистка всех данных перед добавлением новых
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write("✅ Все данные удалены из базы.")

        # Создание тестовых категорий
        categories = [
            {"name": "Рассылки", "description": "Автоматические рассылки"},
            {"name": "Телеграм боты", "description": "Боты для Telegram"},
            {"name": "Полезные утилиты", "description": "Различные полезные инструменты"},
        ]

        created_categories = []
        for cat in categories:
            category = Category.objects.create(**cat)
            created_categories.append(category)

        self.stdout.write(f"➕ Добавлено {len(created_categories)} категорий.")

        # Создание тестовых продуктов
        products_data = [
            {
                "name": "Рассылка новостей",
                "description": "Ежедневная рассылка новостей",
                "price": round(random.uniform(50, 300), 2),
                "category": created_categories[0],
            },
            {
                "name": "Telegram-бот заказов",
                "description": "Бот для автоматизации заказов",
                "price": round(random.uniform(50, 300), 2),
                "category": created_categories[1],
            },
            {
                "name": "Логгер активности",
                "description": "Утилита для логирования действий пользователей",
                "price": round(random.uniform(50, 300), 2),
                "category": created_categories[2],
            },
        ]

        for prod in products_data:
            Product.objects.create(**prod)

        self.stdout.write(f"➕ Добавлено {len(products_data)} продуктов.")