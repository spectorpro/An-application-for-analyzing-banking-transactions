from datetime import datetime
from unittest.mock import mock_open
from unittest.mock import patch

import pandas as pd
import pytest

from src.utils import get_greeting
from src.utils import load_transactions
from src.utils import load_user_settings


class TestLoadTransactions:
    @patch('pandas.read_excel')
    def test_returns_dataframe(self, mock_read_excel):
        test_df = pd.DataFrame({'id': [1, 2], 'amount': [100, 200]})
        mock_read_excel.return_value = test_df
        result = load_transactions('transactions.xlsx')
        assert isinstance(result, pd.DataFrame)
        pd.testing.assert_frame_equal(result, test_df)


class TestGetGreeting:
    @pytest.mark.parametrize("hour,expected", [
        (6, "Доброе утро"),
        (11, "Доброе утро"),
        (12, "Добрый день"),
        (17, "Добрый день"),
        (18, "Добрый вечер"),
        (22, "Добрый вечер"),
        (23, "Доброй ночи"),
        (5, "Доброй ночи"),
    ])
    def test_greeting_by_hour(self, hour, expected):
        test_time = datetime(2023, 1, 1, hour, 0, 0)
        result = get_greeting(test_time)
        assert result == expected


class TestLoadUserSettings:
    def test_loads_valid_json(self):
        json_data = '{"notifications": true, "currency": "RUB"}'
        with patch('builtins.open', mock_open(read_data=json_data)):
            result = load_user_settings('settings.json')
            assert result == {"notifications": True, "currency": "RUB"}

    def test_file_not_found_raises_exception(self):
        with patch('builtins.open', side_effect=FileNotFoundError):
            with pytest.raises(FileNotFoundError):
                load_user_settings('missing.json')
