from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from .forms import ProductForm
from catalog.models import Product
from django.core.cache import cache
from .services import get_products_by_category


def get_products_from_cache():
    """Получить опубликованные продукты из кеша или из БД"""
    queryset = cache.get('published_products')
    if not queryset:
        queryset = Product.objects.filter(is_published=True)
        cache.set('published_products', queryset, 60 * 15)  # кешируем на 15 минут
    return queryset

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return get_products_from_cache()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        for product in context['object_list']:
            product.can_edit = user.is_authenticated and user == product.owner
            product.can_delete = user.is_authenticated and (
                user == product.owner or user.has_perm('catalog.delete_product')
            )
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.is_published and not self.request.user.has_perm('catalog.can_unpublish_product'):
            # Если не опубликован и пользователь не модератор — 404
            from django.http import Http404
            raise Http404("Продукт не опубликован и недоступен.")
        obj.views_counter += 1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        product = context['object']

        # Добавляем флаги только для этого продукта
        context['can_edit'] = user.is_authenticated and user == product.owner
        context['can_delete'] = user.is_authenticated and (
                user == product.owner or user.has_perm('catalog.delete_product')
        )
        return context

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = '/users/login/'  # Куда перенаправить, если не авторизован

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)  # ← сначала сохраняем
        # Очищаем кеш категории
        cache.delete(f'products_category_{self.object.category}')
        return response


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = '/users/login/'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Проверяем: владелец или модератор?
        if obj.owner != self.request.user and not self.request.user.has_perm('catalog.can_unpublish_product'):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("Вы не можете редактировать этот продукт.")
        return obj

    def form_valid(self, form):
        response = super().form_valid(form)
        # Очищаем кеш старой и новой категории (если изменилась)
        cache.delete(f'products_category_{self.object.category}')
        return response

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = '/users/login/'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Владелец или модератор может удалять
        if obj.owner != self.request.user and not self.request.user.has_perm('catalog.delete_product'):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("Вы не можете удалить этот продукт.")
        return obj

    def delete(self, request, *args, **kwargs):
        # Сохраняем категорию до удаления
        category = self.get_object().category
        response = super().delete(request, *args, **kwargs)
        # Очищаем кеш категории
        cache.delete(f'products_category_{category}')
        return response

class HomeView(TemplateView):
    template_name = "catalog/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = get_products_from_cache()  # ← из кеша
        user = self.request.user
        for product in context['object_list']:
            product.can_edit = user.is_authenticated and user == product.owner
            product.can_delete = user.is_authenticated and (
                    user == product.owner or user.has_perm('catalog.delete_product')
            )
        return context

class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"

# Отдельный вью для отмены публикации
class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'catalog.can_unpublish_product'

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.is_published:
            product.is_published = False
            product.save()
            messages.success(request, f"Продукт '{product.name}' снят с публикации.")
        return redirect('catalog:product_list')

class ProductCategoryView(View):
    """
    Отображает все продукты в указанной категории.
    URL: /category/electronics/
    """
    def get(self, request, category_name):
        products = get_products_by_category(category_name)

        if not products.exists():
            # Можно показать, что товаров нет
            pass

        return render(request, 'catalog/product_category.html', {
            'products': products,
            'category_name': category_name.capitalize(),
        })

class CategoryListView(TemplateView):
    template_name = 'catalog/category_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем все категории с опубликованными товарами
        categories = Product.objects.filter(
            is_published=True,
            category__isnull=False
        ).values_list('category__name', flat=True).distinct()
        context['categories'] = categories
        return context