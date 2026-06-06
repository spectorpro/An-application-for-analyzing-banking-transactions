import pytest
import pandas as pd
from datetime import datetime
from unittest.mock import patch, Mock
from src.views import generate_main_page_json

class TestGenerateMainPageJson:
    @pytest.fixture
    def sample_transactions(self):
        """Фикстура с тестовыми транзакциями."""
        return pd.DataFrame({
            'Дата операции': [
                '01.01.2023 10:30:00',
                '15.01.2023 14:20:00',
                '20.01.2023 09:15:00'
            ],
            'Номер карты': ['1234567890123456', '1234567890123457', '1234567890123456'],
            'Сумма операции': [1000.50, 2500.75, 1500.25],
            'Категория': ['Продукты', 'Развлечения', 'Продукты'],
            'Описание': ['Супермаркет', 'Кинотеатр', 'Магазин у дома']
        })

    @pytest.fixture
    def user_settings(self):
        """Фикстура с настройками пользователя."""
        return {
            'cashback_rate': 0.02,
            'user_currencies': ['USD', 'EUR'],
            'user_stocks': ['AAPL', 'GOOGL']
        }

    def test_valid_input_returns_correct_structure(self, sample_transactions, user_settings):
        """Тест: корректные входные данные возвращают JSON с правильной структурой."""
        input_date = '2023-01-20 00:00:00'
        end_date = datetime(2023, 1, 20)

        result = generate_main_page_json(input_date, sample_transactions, user_settings, end_date)

        assert isinstance(result, dict)
        assert 'greeting' in result
        assert 'cards' in result
        assert 'top_transactions' in result
        assert 'currency_rates' in result
        assert 'stock_prices' in result

    def test_incorrect_date_format_raises_value_error(self, sample_transactions, user_settings):
        """Тест: некорректный формат даты вызывает ValueError."""
        input_date = 'invalid-date-format'
        end_date = datetime(2023, 1, 20)

        with pytest.raises(ValueError, match="Некорректный формат даты input_date"):
            generate_main_page_json(input_date, sample_transactions, user_settings, end_date)

    @patch('src.views.get_greeting')
    def test_greeting_called_with_correct_date(self, mock_get_greeting, sample_transactions, user_settings):
        """Тест: приветствие вызывается с правильной датой."""
        mock_get_greeting.return_value = "Доброе утро!"
        input_date = '2023-01-15 08:30:00'
        end_date = datetime(2023, 1, 15)

        generate_main_page_json(input_date, sample_transactions, user_settings, end_date)

        mock_get_greeting.assert_called_once_with(datetime(2023, 1, 15, 8, 30, 0))


    @patch('src.views.get_currency_rates')
    def test_currency_rates_called_with_user_currencies(self, mock_get_currency_rates, sample_transactions, user_settings):
        """Тест: курсы валют запрашиваются для валют пользователя."""
        mock_get_currency_rates.return_value = {'USD': 75.50, 'EUR': 82.30}
        input_date = '2023-01-20 00:00:00'
        end_date = datetime(2023, 1, 20)

        generate_main_page_json(input_date, sample_transactions, user_settings, end_date)

        mock_get_currency_rates.assert_called_once_with(['USD', 'EUR'])

    @patch('src.views.get_stock_prices')
    def test_stock_prices_called_with_user_stocks(self, mock_get_stock_prices, sample_transactions, user_settings):
        """Тест: цены акций запрашиваются для акций пользователя."""
        mock_get_stock_prices.return_value = {'AAPL': 175.50, 'GOOGL': 2800.00}
        input_date = '2023-01-20 00:00:00'
        end_date = datetime(2023, 1, 20)

        generate_main_page_json(input_date, sample_transactions, user_settings, end_date)

        mock_get_stock_prices.assert_called_once_with(['AAPL', 'GOOGL'])

    def test_empty_transactions_returns_empty_cards_and_top_transactions(self, user_settings):
        """Тест: пустые транзакции возвращают пустые списки карт и топ-транзакций."""
        empty_transactions = pd.DataFrame(
            columns=['Дата операции', 'Номер карты', 'Сумма операции', 'Категория', 'Описание'])
        input_date = '2023-01-20 00:00:00'
        end_date = datetime(2023, 1, 20)

        result = generate_main_page_json(input_date, empty_transactions, user_settings, end_date)

        # Дополнительно: добавьте проверки результата
        assert result['cards'] == []
        assert result['top_transactions'] == []
