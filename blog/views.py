
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy, reverse
from .models import BlogPost
from django.core.mail import send_mail
from django.conf import settings


class BlogPostListView(ListView):
    model = BlogPost
    template_name = "blog/post_list.html"
    context_object_name = "posts"

    # 🔹 Фильтрация: только опубликованные статьи
    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    # 🔹 Увеличение счётчика просмотров
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()

        # 🔔 Отправка уведомления на почту при достижении 100 просмотров
        if obj.views_count == 100:
            send_mail(
                subject=f"🎉 Поздравляем! Статья '{obj.title}' достигла 100 просмотров!",
                message=(
                    f"Ваша статья '{obj.title}' успешно набрала 100 просмотров.\n"
                    f"Дата: {obj.created_at.strftime('%d.%m.%Y')}\n"
                    f"Спасибо за качественный контент!"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['your-email@example.com'],  # ← Замените на свою почту
                fail_silently=False,
            )
        return obj

class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ["title", "content", "preview", "is_published"]
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("blog:post_list")


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ["title", "content", "preview", "is_published"]
    template_name = "blog/post_form.html"

    # 🔹 Перенаправление на страницу статьи после редактирования
    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.object.pk})


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")