import requests


def get_currency_rates(currencies: list) -> list:
    """Получение курсов валют (используем free API)"""
    rates = []
    for currency in currencies:
        try:
            # Используем бесплатный API для курсов валют
            response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{currency}")
            data = response.json()
            rates.append({
                "currency": currency,
                "rate": float(data['rates']['RUB'])
            })
        except Exception as e:
            print(f"Ошибка получения курса для {currency}: {e}")
            rates.append({"currency": currency, "rate": 0.0})
    return rates


def get_stock_prices(stocks: list) -> list:
    """Получение цен акций (используем бесплатный API)"""
    prices = []
    # Для примера используем статические данные или бесплатный API
    stock_data = {
        "AAPL": 150.12,
        "AMZN": 3173.18,
        "GOOGL": 2742.39,
        "MSFT": 296.71,
        "TSLA": 1007.08
    }
    for stock in stocks:
        prices.append({
            "stock": stock,
            "price": stock_data.get(stock, 0.0)
        })
    return prices
