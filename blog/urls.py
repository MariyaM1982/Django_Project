from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.BlogPostListView.as_view(), name="post_list"),
    path("post/<int:pk>/", views.BlogPostDetailView.as_view(), name="post_detail"),
    path("create/", views.BlogPostCreateView.as_view(), name="post_create"),
    path("edit/<int:pk>/", views.BlogPostUpdateView.as_view(), name="post_update"),
    path("delete/<int:pk>/", views.BlogPostDeleteView.as_view(), name="post_delete"),
]