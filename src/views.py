from datetime import datetime
from typing import Dict

import pandas as pd

from .services import get_currency_rates
from .services import get_stock_prices
from .utils import get_greeting


def generate_main_page_json(
    input_date: str,
    transactions: pd.DataFrame,
    user_settings: Dict,
    end_date: datetime
) -> Dict:
    """
    Генерирует JSON для главной страницы с данными о транзакциях, картах, курсах валют и акциях.

    Args:
        input_date: Дата начала периода в формате '%Y-%m-%d %H:%M:%S' (строка)
        transactions: DataFrame с транзакциями (колонки: 'Дата операции', 'Номер карты', 'Сумма операции' и т.д.)
        user_settings: Настройки пользователя (валюты, акции и т.п.)
        end_date: Конечная дата периода (datetime)

    Returns:
        Словарь с данными для отображения на главной странице
    """
    # Парсим входную дату единожды
    try:
        start_date = datetime.strptime(input_date, '%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        raise ValueError(f"Некорректный формат даты input_date: {e}")

    # Преобразуем колонку с датами к формату datetime, если ещё не преобразована
    if not pd.api.types.is_datetime64_any_dtype(transactions['Дата операции']):
        transactions['Дата операции'] = pd.to_datetime(
            transactions['Дата операции'],
            format='%d.%m.%Y %H:%M:%S',
            dayfirst=True,
            errors='coerce'  # Пропускаем некорректные даты
        )
        # Удаляем строки с некорректными датами
        transactions = transactions.dropna(subset=['Дата операции'])

    # Фильтруем транзакции за нужный период (с начала месяца до указанной даты)
    month_start = start_date.replace(day=1, hour=0, minute=0, second=0)
    filtered_transactions = transactions[
        (transactions['Дата операции'] >= month_start) &
        (transactions['Дата операции'] <= end_date)
    ]

    # Получаем приветствие
    greeting = get_greeting(start_date)

    # Обработка карт и расчёт расходов/кешбэка
    cashback_rate = user_settings.get('cashback_rate', 0.01)  # % кешбэка из настроек
    cards_data = []

    if not filtered_transactions.empty:
        card_groups = filtered_transactions.groupby('Номер карты')
        for card_number, group in card_groups:
            total_spent = group['Сумма операции'].sum()
            cashback = total_spent * cashback_rate
            cards_data.append({
                "last_digits": str(card_number)[-4:],
                "total_spent": round(total_spent, 2),
                "cashback": round(cashback, 2)
            })

    # Топ-5 транзакций по сумме
    top_transactions_list = []
    if not filtered_transactions.empty:
        top_transactions = filtered_transactions.nlargest(5, 'Сумма операции')
        for _, row in top_transactions.iterrows():
            top_transactions_list.append({
                "date": row['Дата операции'].strftime('%d.%m.%Y'),
                "amount": round(row['Сумма операции'], 2),
                "category": row.get('Категория', 'Не указана'),
                "description": row.get('Описание', 'Нет описания')
            })

    # Курсы валют
    user_currencies = user_settings.get('user_currencies', [])
    currency_rates = get_currency_rates(user_currencies) if user_currencies else {}

    # Цены акций
    user_stocks = user_settings.get('user_stocks', [])
    stock_prices = get_stock_prices(user_stocks) if user_stocks else {}

    return {
        "greeting": greeting,
        "cards": cards_data,
        "top_transactions": top_transactions_list,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }
