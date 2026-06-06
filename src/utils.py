import pandas as pd
from datetime import datetime
import json

def load_transactions(file_path: str) -> pd.DataFrame:
    """Загрузка транзакций из Excel-файла"""
    return pd.read_excel(file_path)

def get_greeting(current_time: datetime) -> str:
    """Возвращает приветствие в зависимости от времени суток"""
    hour = current_time.hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"

def load_user_settings(settings_path: str) -> dict:
    """Загрузка пользовательских настроек"""
    with open(settings_path, 'r', encoding='utf-8') as f:
        return json.load(f)
