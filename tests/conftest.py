"""
Configuração do pytest para os testes do Crypto Tracker.
"""

import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import Mock, patch

from crypto_tracker import CryptoTracker, DatabaseManager, TelegramNotifier, ChartGenerator
from crypto_tracker.config import config


@pytest.fixture
def sample_crypto_data():
    """Retorna dados de exemplo de criptomoedas."""
    return [
        {
            'name': 'Bitcoin',
            'market_cap': 'US$1,000,000,000,000',
            'price': 'US$50,000',
            'volume_24h': 'US$30,000,000,000',
            'change_24h': '+2.5%'
        },
        {
            'name': 'Ethereum',
            'market_cap': 'US$500,000,000,000',
            'price': 'US$2,500',
            'volume_24h': 'US$15,000,000,000',
            'change_24h': '-1.2%'
        }
    ]


@pytest.fixture
def sample_crypto_dataframe(sample_crypto_data):
    """Retorna um DataFrame com dados de exemplo."""
    return pd.DataFrame(sample_crypto_data)


@pytest.fixture
def mock_driver():
    """Retorna um mock do driver do Selenium."""
    driver = Mock()
    driver.get = Mock()
    driver.find_elements = Mock(return_value=[])
    driver.quit = Mock()
    return driver


@pytest.fixture
def crypto_tracker():
    """Retorna uma instância do CryptoTracker."""
    return CryptoTracker()


@pytest.fixture
def database_manager():
    """Retorna uma instância do DatabaseManager."""
    return DatabaseManager()


@pytest.fixture
def telegram_notifier():
    """Retorna uma instância do TelegramNotifier."""
    return TelegramNotifier()


@pytest.fixture
def chart_generator():
    """Retorna uma instância do ChartGenerator."""
    return ChartGenerator()


@pytest.fixture
def temp_output_dir(tmp_path):
    """Retorna um diretório temporário para saída."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir
