import json
import logging
from datetime import datetime

import pandas as pd

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/utils.log', encoding='utf-8'),  # Логи в файл
        logging.StreamHandler()  # Вывод логов в консоль
    ]
)
logger = logging.getLogger(__name__)


def load_transactions(file_path: str) -> pd.DataFrame:
    """Загрузка транзакций из Excel-файла"""
    try:
        logger.info(f"Начинается загрузка транзакций из файла: {file_path}")
        df = pd.read_excel(file_path)
        logger.info(f"Успешно загружено {len(df)} строк транзакций")
        return df
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Ошибка при загрузке файла {file_path}: {str(e)}")
        raise


def get_greeting(current_time: datetime) -> str:
    """Возвращает приветствие в зависимости от времени суток"""
    hour = current_time.hour
    logger.debug(f"Определяется приветствие для часа: {hour}")

    if 6 <= hour < 12:
        greeting = "Доброе утро"
    elif 12 <= hour < 18:
        greeting = "Добрый день"
    elif 18 <= hour < 23:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"

    logger.info(f"Сгенерировано приветствие: '{greeting}' для времени {current_time.strftime('%H:%M')}")
    return greeting


def load_user_settings(settings_path: str) -> dict:
    """Загрузка пользовательских настроек"""
    try:
        logger.info(f"Начинается загрузка настроек из файла: {settings_path}")
        with open(settings_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        logger.info(f"Настройки успешно загружены. Найдено {len(settings)} параметров")
        return settings
    except FileNotFoundError:
        logger.error(f"Файл настроек не найден: {settings_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка парсинга JSON в файле {settings_path}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка при загрузке настроек {settings_path}: {str(e)}")
        raise
