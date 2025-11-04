from django.urls import path
from catalog import views
from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, \
    ContactsView, HomeView

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path('catalog/<int:pk>/', ProductDetailView.as_view(), name="product_detail"),
    path('catalog/create/', ProductCreateView.as_view(), name="product_create"),
    path('catalog/<int:pk>/update/', ProductUpdateView.as_view(), name="product_update"),
    path('catalog/<int:pk>/delete/', ProductDeleteView.as_view(), name="product_delete"),
]
