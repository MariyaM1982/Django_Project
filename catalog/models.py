from django.conf import settings
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
    image = models.ImageField(upload_to="products/images/", blank=True, null=True, verbose_name="Изображение")
    preview = models.ImageField(upload_to="catalog/previews/", null=True, blank=True, verbose_name="Превью")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL,null=True, related_name="products", verbose_name="Категория")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за покупку")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")
    views_counter = models.PositiveIntegerField(verbose_name="Cчетчик просмотров", help_text="Укажите количество просмотров", default=0)
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")

    # Поле владельца
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Владелец",
        null=False,
        blank=False
    )


    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "created_at", "price", "category"]
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
        ]

    def __str__(self):
        return self.name
