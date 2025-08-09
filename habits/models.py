from django.db import models

from config import settings


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Укажите пользователя',
    )
    place = models.CharField(
        max_length=150,
        verbose_name='Место',
        help_text='Укажите место',
        blank=True,
        null=True,
    )
    time = models.CharField(
        max_length=150,
        verbose_name='Время',
        help_text='Укажите время',
        blank=True,
        null=True,
    )
    action = models.CharField(
        max_length=250,
        verbose_name='Действие',
        help_text='Укажите действие'
    )
    is_pleasant = models.BooleanField(
        verbose_name='Является ли приятной привычкой',
        help_text='Укажите, является ли приятной привычкой',
    )
    related_habit = models.ForeignKey('Habit',
        on_delete=models.SET_NULL,
        verbose_name='Связанная привычка',
        help_text='Укажите связанную привычку',
        related_name='habits',
        blank=True,
        null=True,
    )
    interval = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Периодичность',
        help_text='Укажите периодичность',
    )
    award = models.CharField(
        max_length=150,
        verbose_name='Вознаграждение',
        help_text='Укажите вознаграждение',
        blank=True,
        null=True,
    )
    time_to_complete = models.DurationField(
        verbose_name='Время на выполнение',
        help_text='Укажите время на выполнение',
        blank=True,
        null=True,
    )
    is_public = models.BooleanField(
        verbose_name='Является ли публичной',
        help_text='Укажите, является ли привычка публичной',
    )


    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f'Я буду {self.action} в {self.time} в {self.place}'
