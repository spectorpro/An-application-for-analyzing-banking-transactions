import pandas as pd
from datetime import datetime
from src.utils import load_transactions, load_user_settings
from src.views import generate_main_page_json
import json
import os

def main():
    # Определяем пути относительно текущей директории
    current_dir = os.path.dirname(os.path.abspath(__file__))
    transactions_path = os.path.join(current_dir, 'data', 'operations.xlsx')
    settings_path = os.path.join(current_dir, 'user_settings.json')

    try:
        # Загрузка данных
        transactions = load_transactions(transactions_path)
        user_settings = load_user_settings(settings_path)

        # Устанавливаем end_date как текущую дату
        end_date = datetime.now()

        # Пример вызова для главной страницы
        input_date = '2023-05-20 14:30:00'
        result = generate_main_page_json(input_date, transactions, user_settings, end_date)

        # Вывод результата
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except FileNotFoundError as e:
        print(f"Ошибка: Файл не найден — {e}")
    except Exception as e:
        print(f"Произошла ошибка при выполнении: {e}")

if __name__ == '__main__':
    main()
