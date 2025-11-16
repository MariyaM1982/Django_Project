from django.core.cache import cache

from config.settings import CACHE_ENABLED
from catalog.models import Product

def get_products_from_cache():
    if not CACHE_ENABLED:
        return Product.objects.all()
    key = 'products_list'
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.all()
    cache.set(key, products)
    return products

def get_products_by_category(category_name, use_cache=True):
    """
    Возвращает список продуктов в указанной категории (по имени категории, без учёта регистра).
    """
    if not category_name:
        return Product.objects.none()

    cache_key = f'products_category_{category_name.lower()}'

    if use_cache:
        products = cache.get(cache_key)
        if products is not None:
            return products

    # Фильтруем по полю `name` в модели Category, без учёта регистра
    products = Product.objects.filter(
        category__name__iexact=category_name,
        is_published=True
    )

    if use_cache:
        cache.set(cache_key, products, 60 * 15)  # 15 минут

    return products

