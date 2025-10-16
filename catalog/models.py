# catalog/models.py
from django.db import models
from django.utils import timezone


class Category(models.Model):
    """
    Модель категории продуктов.
    """

    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]  # сортировка по имени

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Модель продукта.
    """

    name = models.CharField(max_length=200, verbose_name="Наименование")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    image = models.ImageField(
        upload_to="products/images/", blank=True, null=True, verbose_name="Изображение"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="products",
        verbose_name="Категория",
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена за покупку"
    )
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения"
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = [
            "created_at",
            "price",
            "category",
        ]  # сортировка по дате создания (сверху новые)

    def __str__(self):
        return self.name
