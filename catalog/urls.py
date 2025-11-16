from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.decorators.cache import cache_page
from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, \
    ContactsView, HomeView, ProductUnpublishView, ProductCategoryView, CategoryListView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),  # Главная — это список товаров
    path('home/', HomeView.as_view(), name='home'),  # Дополнительно: /home/
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('unpublish/<int:pk>/', ProductUnpublishView.as_view(), name='product_unpublish'),
    path('users/', include('users.urls')),
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/<str:category_name>/', ProductCategoryView.as_view(), name='product_category'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)