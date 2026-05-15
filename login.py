from instagrapi import Client
import json

# Вставь сюда скопированное значение целиком
SESSION_ID = "" 

cl = Client()

try:
    print("Пробую войти по sessionid...")
    cl.login_by_sessionid(SESSION_ID)
    
    # Проверка, что логин прошел успешно
    user_info = cl.account_info()
    print(f"Успешный вход! Аккаунт: {user_info.username}")
    
    # Сохраняем настройки в файл, который использует твой основной бот
    cl.dump_settings("session.json")
    print("Файл session.json обновлен. Теперь можешь запускать основной воркер.")

except Exception as e:
    print(f"Ошибка при входе: {e}")