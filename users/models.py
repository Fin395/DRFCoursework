from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Укажите email"
    )

    phone_number = models.CharField(
        max_length=25,
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="Укажите номер телефона",
    )

    city = models.CharField(
        max_length=100,
        verbose_name="Город",
        blank=True,
        null=True,
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Загрузите свой аватар",
    )
    tg_chat_id = models.CharField(
        max_length=50,
        verbose_name="Телеграм chat-id",
        blank=True,
        null=True,
        help_text="Укажите телеграм chat-id",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
