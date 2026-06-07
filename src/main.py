import json
import logging
import os
from argparse import ArgumentParser
from datetime import datetime

from src.utils import load_transactions
from src.utils import load_user_settings
from src.views import generate_main_page_json

# Настройка логирования с корректным путём для Windows
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)  # Создаём директорию, если её нет
log_file_path = os.path.join(log_dir, 'main.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def parse_arguments():
    """Парсинг аргументов командной строки."""
    parser = ArgumentParser(description='Анализ банковских транзакций')
    parser.add_argument(
        '--input-date',
        type=str,
        default=None,
        help='Дата для анализа в формате YYYY-MM-DD HH:MM:SS (по умолчанию — текущая дата)'
    )
    parser.add_argument(
        '--transactions-path',
        type=str,
        default='data/operations.xlsx',
        help='Путь к файлу с транзакциями'
    )
    parser.add_argument(
        '--settings-path',
        type=str,
        default='user_settings.json',
        help='Путь к файлу настроек пользователя'
    )
    return parser.parse_args()


def validate_data(transactions, user_settings):
    """Валидация загруженных данных."""
    if transactions.empty:
        raise ValueError("Файл транзакций пуст")
    if user_settings is None:
        raise ValueError("Настройки пользователя не загружены")
    logger.info(f"Загружено {len(transactions)} транзакций")
    return True


def main():
    try:
        # Парсинг аргументов
        args = parse_arguments()

        # Определяем пути относительно текущей директории
        current_dir = os.path.dirname(os.path.abspath(__file__))
        transactions_path = os.path.join(current_dir, args.transactions_path)
        settings_path = os.path.join(current_dir, args.settings_path)

        logger.info(f"Загрузка транзакций из: {transactions_path}")
        logger.info(f"Загрузка настроек из: {settings_path}")

        # Загрузка данных
        transactions = load_transactions(transactions_path)
        user_settings = load_user_settings(settings_path)

        # Валидация данных
        validate_data(transactions, user_settings)

        # Устанавливаем даты
        end_date = datetime.now()
        input_date_str = args.input_date or end_date.strftime('%Y-%m-%d %H:%M:%S')
        start_date = datetime.strptime(input_date_str, '%Y-%m-%d %H:%M:%S')

        logger.info(f"Анализ на дату: {input_date_str}")

        result = generate_main_page_json(input_date_str, transactions, user_settings, end_date)

        # Вывод результата
        print(json.dumps(result, ensure_ascii=False, indent=2))
        logger.info("Выполнение завершено успешно")

    except FileNotFoundError as e:
        logger.error(f"Файл не найден: {e}")
        print(f"Ошибка: Файл не найден — {e}")
    except ValueError as e:
        logger.error(f"Ошибка валидации данных: {e}")
        print(f"Ошибка данных: {e}")
    except Exception as e:
        logger.exception(f"Неожиданная ошибка: {e}")
        print(f"Произошла ошибка при выполнении: {e}")


if __name__ == '__main__':
    main()
