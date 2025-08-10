from config import settings
import requests

def send_telegram_message(chat_id, message):
    params = {
        'text': message,
        'chat_id': chat_id
    }
    try:
        requests.get(f'{settings.TELEGRAM_URL}{settings.TG_BOT_TOKEN}/sendMessage', params=params)
    except Exception as e:
        print(f'Во время отправки сообщения для {chat_id} произошла ошибка {e}')
