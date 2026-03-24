"""
Testes do módulo tracker.
"""

import pytest
from unittest.mock import Mock, patch
import pandas as pd

from crypto_tracker.tracker import CryptoTracker
from crypto_tracker.config import config


class TestCryptoTracker:
    """Testes da classe CryptoTracker."""
    
    def test_initialization(self):
        """Testa a inicialização do CryptoTracker."""
        with patch('crypto_tracker.tracker.uc.Chrome'):
            tracker = CryptoTracker()
            assert tracker.telegram is not None
            assert tracker.database is not None
            assert tracker.chart_generator is not None
    
    @patch('crypto_tracker.tracker.uc.Chrome')
    def test_collect_crypto_data(self, mock_chrome):
        """Testa a coleta de dados de criptomoedas."""
        # Configura mock do driver
        mock_driver = Mock()
        mock_driver.get = Mock()
        mock_driver.find_elements = Mock(return_value=[])
        mock_chrome.return_value = mock_driver
        
        tracker = CryptoTracker()
        crypto_data = tracker.collect_crypto_data()
        
        assert isinstance(crypto_data, list)
    
    @patch('crypto_tracker.tracker.uc.Chrome')
    def test_get_status(self, mock_chrome):
        """Testa a obtenção do status do rastreador."""
        mock_driver = Mock()
        mock_driver.get = Mock()
        mock_driver.find_elements = Mock(return_value=[])
        mock_chrome.return_value = mock_driver
        
        tracker = CryptoTracker()
        status = tracker.get_status()
        
        assert 'database_path' in status
        assert 'record_count' in status
        assert 'crypto_count' in status
        assert 'telegram_configured' in status
