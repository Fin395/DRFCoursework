from celery import shared_task

from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def send_tg_notification():
    all_habits_to_send = Habit.objects.filter(user__tg_chat_id__isnull=False).filter(is_pleasant=False)
    if all_habits_to_send.exists():
        for habit in all_habits_to_send:
            user_name = habit.user.tg_chat_id
            message = f'Уважаемый пользователь с ID:{user_name}! Напоминаем, что вам завтра необходимо: {habit.action} в {habit.time} {habit.place}'
            print(habit.user.tg_chat_id)
            send_telegram_message(habit.user.tg_chat_id, message)
