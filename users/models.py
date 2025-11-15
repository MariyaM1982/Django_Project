# from django.contrib.auth.base_user import BaseUserManager
# from django.contrib.auth.models import AbstractUser
# from django.db import models
#
#
# class UserManager(BaseUserManager):
#     """Кастомный менеджер для использования email как уникального поля"""
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('Email обязателен')
#         email = self.normalize_email(email)
#         # extra_fields.pop(None)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)
#
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Суперпользователь должен иметь is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Суперпользователь должен иметь is_superuser=True.')
#
#         # Устанавливаем username=None, если не передан
#         # extra_fields.setdefault(None)
#         return self.create_user(email, password, **extra_fields)
#
# class User(AbstractUser):
#     # username = None
#     email = models.EmailField(verbose_name='Email', unique=True)  # Делаем email уникальным и основным полем для входа
#
#     phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон", help_text="Введите номер телефона")
#     country = models.CharField(max_length=100, blank=True, null=True, verbose_name="Страна", help_text="Введите страну")
#     avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True, verbose_name="Аватар")
#
#     # Указываем, что логин — через email
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#
#     objects = UserManager()
#
#     class Meta:
#         verbose_name = "Пользователь"
#         verbose_name_plural = "Пользователи"
#
#     def __str__(self):
#         return self.email

# users/models.py
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        extra_fields.pop('username', None)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.pop('username', None)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='Email', unique=True)

    phone = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email