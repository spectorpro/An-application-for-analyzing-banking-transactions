import unittest
from unittest.mock import patch, Mock
import requests

from src.services import get_currency_rates, get_stock_prices

class TestCurrencyRates(unittest.TestCase):

        @patch('requests.get')
        def test_get_currency_rates_success(self, mock_get):
            """Тест успешного получения курсов валют"""
            # Настраиваем mock для успешного ответа API
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'rates': {'RUB': 90.5}
            }
            mock_get.return_value = mock_response

            # Тестируем функцию
            result = get_currency_rates(['USD'])

            # Проверяем результат
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['currency'], 'USD')
            self.assertEqual(result[0]['rate'], 90.5)

        @patch('requests.get')
        def test_get_currency_rates_multiple_currencies(self, mock_get):
            """Тест получения курсов для нескольких валют"""

            def side_effect(url):
                if 'USD' in url:
                    mock = Mock()
                    mock.status_code = 200
                    mock.json.return_value = {'rates': {'RUB': 90.5}}
                    return mock
                elif 'EUR' in url:
                    mock = Mock()
                    mock.status_code = 200
                    mock.json.return_value = {'rates': {'RUB': 100.2}}
                    return mock
                else:
                    raise Exception("Unknown currency")

            mock_get.side_effect = side_effect

            result = get_currency_rates(['USD', 'EUR'])

            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]['currency'], 'USD')
            self.assertEqual(result[0]['rate'], 90.5)
            self.assertEqual(result[1]['currency'], 'EUR')
            self.assertEqual(result[1]['rate'], 100.2)

        @patch('requests.get')
        def test_get_currency_rates_api_error(self, mock_get):
            """Тест обработки ошибки API"""
            # Симулируем ошибку подключения
            mock_get.side_effect = requests.exceptions.RequestException("Connection error")

            result = get_currency_rates(['USD'])

            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['currency'], 'USD')
            self.assertEqual(result[0]['rate'], 0.0)

        @patch('requests.get')
        def test_get_currency_rates_invalid_json(self, mock_get):
            """Тест обработки некорректного JSON ответа"""
            mock_response = Mock()
            mock_response.status_code = 200
            # Симулируем отсутствие нужного поля в JSON
            mock_response.json.return_value = {'error': 'Invalid currency'}
            mock_get.return_value = mock_response

            result = get_currency_rates(['INVALID'])

            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['currency'], 'INVALID')
            self.assertEqual(result[0]['rate'], 0.0)


class TestStockPrices(unittest.TestCase):

    def test_get_stock_prices_existing_stocks(self):
        """Тест получения цен для существующих акций"""
        result = get_stock_prices(['AAPL', 'MSFT'])

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['stock'], 'AAPL')
        self.assertEqual(result[0]['price'], 150.12)
        self.assertEqual(result[1]['stock'], 'MSFT')
        self.assertEqual(result[1]['price'], 296.71)

    def test_get_stock_prices_non_existent_stock(self):
        """Тест для несуществующей акции"""
        result = get_stock_prices(['NONEXISTENT'])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['stock'], 'NONEXISTENT')
        self.assertEqual(result[0]['price'], 0.0)

    def test_get_stock_prices_mixed_stocks(self):
        """Тест для смеси существующих и несуществующих акций"""
        result = get_stock_prices(['AAPL', 'NONEXISTENT', 'GOOGL'])

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['stock'], 'AAPL')
        self.assertEqual(result[0]['price'], 150.12)
        self.assertEqual(result[1]['stock'], 'NONEXISTENT')
        self.assertEqual(result[1]['price'], 0.0)
        self.assertEqual(result[2]['stock'], 'GOOGL')
        self.assertEqual(result[2]['price'], 2742.39)

    def test_get_stock_prices_empty_list(self):
        """Тест для пустого списка акций"""
        result = get_stock_prices([])

        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()
