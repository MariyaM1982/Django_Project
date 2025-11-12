from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView
from users.forms import UserRegisterForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        # Сохраняем пользователя
        response = super().form_valid(form)

        # Данные пользователя
        user = form.instance
        email = user.email

        # Отправка письма
        try:
            send_mail(
                subject='Добро пожаловать!',
                message=f'Привет, {user.username}! Спасибо за регистрацию на нашем сайте.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            # Опционально: показать сообщение
            messages.success(self.request, 'Письмо с приветствием отправлено на ваш email.')
        except Exception as e:
            messages.error(self.request, f'Не удалось отправить письмо: {e}')

        return response