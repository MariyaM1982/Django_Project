from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Настройка отображения модели Category в админке.
    """
    list_display = ("id", "name")  # Поля, отображаемые в списке
    search_fields = ("name",)      # Поиск по имени категории
    ordering = ("name",)           # Сортировка по имени


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Настройка отображения модели Product в админке.
    """
    list_display = ("id", "name", "price", "category")  # Поля, отображаемые в списке
    list_filter = ("category",)                        # Фильтрация по категории
    search_fields = ("name", "description")            # Поиск по названию и описанию
    ordering = ("-created_at",)                        # Сортировка по дате создания (сверху новые)from django.contrib import admin

# Register your models here.
