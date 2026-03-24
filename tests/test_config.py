"""
Testes do módulo de configuração.
"""

import pytest
from pathlib import Path

from crypto_tracker.config import (
    Config,
    TelegramConfig,
    WebDriverConfig,
    ScrapingConfig,
    DatabaseConfig,
    AlertConfig,
    ChartConfig,
    ScheduleConfig,
    LogConfig,
    OutputConfig,
    ProxyConfig,
    RateLimitingConfig,
    NotificationConfig
)


class TestTelegramConfig:
    """Testes da configuração do Telegram."""
    
    def test_telegram_not_configured(self):
        """Testa quando o Telegram não está configurado."""
        config = TelegramConfig()
        assert not config.is_configured
    
    def test_telegram_configured(self, monkeypatch):
        """Testa quando o Telegram está configurado."""
        monkeypatch.setenv('TELEGRAM_BOT_TOKEN', 'test_token')
        monkeypatch.setenv('TELEGRAM_CHAT_ID', 'test_chat_id')
        
        config = TelegramConfig()
        assert config.is_configured
        assert config.bot_token == 'test_token'
        assert config.chat_id == 'test_chat_id'
    
    def test_telegram_validation_error(self, monkeypatch):
        """Testa erro de validação do Telegram."""
        monkeypatch.setenv('TELEGRAM_BOT_TOKEN', '')
        monkeypatch.setenv('TELEGRAM_CHAT_ID', '')
        
        config = TelegramConfig()
        with pytest.raises(ValueError, match="Token ou Chat ID do Telegram não foram configurados"):
            config.validate()


class TestWebDriverConfig:
    """Testes da configuração do WebDriver."""
    
    def test_default_webdriver_config(self):
        """Testa a configuração padrão do WebDriver."""
        config = WebDriverConfig()
        assert config.browser == 'chrome'
        assert config.headless == True
        assert config.page_load_timeout == 30
        assert config.element_wait_timeout == 10
    
    def test_custom_webdriver_config(self, monkeypatch):
        """Testa configuração personalizada do WebDriver."""
        monkeypatch.setenv('WEBDRIVER_BROWSER', 'firefox')
        monkeypatch.setenv('WEBDRIVER_HEADLESS', 'false')
        monkeypatch.setenv('PAGE_LOAD_TIMEOUT', '60')
        
        config = WebDriverConfig()
        assert config.browser == 'firefox'
        assert config.headless == False
        assert config.page_load_timeout == 60


class TestScrapingConfig:
    """Testes da configuração de scraping."""
    
    def test_default_scraping_config(self):
        """Testa a configuração padrão de scraping."""
        config = ScrapingConfig()
        assert config.max_cryptos == 10
        assert config.coingecko_url == 'https://www.coingecko.com/pt'
    
    def test_custom_scraping_config(self, monkeypatch):
        """Testa configuração personalizada de scraping."""
        monkeypatch.setenv('MAX_CRYPTOS', '20')
        monkeypatch.setenv('COINGECKO_URL', 'https://custom.url')
        
        config = ScrapingConfig()
        assert config.max_cryptos == 20
        assert config.coingecko_url == 'https://custom.url'


class TestDatabaseConfig:
    """Testes da configuração do banco de dados."""
    
    def test_default_database_config(self):
        """Testa a configuração padrão do banco de dados."""
        config = DatabaseConfig()
        assert config.path == 'data/crypto_data.db'
        assert config.backup_enabled == True
    
    def test_custom_database_config(self, monkeypatch):
        """Testa configuração personalizada do banco de dados."""
        monkeypatch.setenv('DATABASE_PATH', 'custom.db')
        monkeypatch.setenv('DATABASE_BACKUP_ENABLED', 'false')
        
        config = DatabaseConfig()
        assert config.path == 'custom.db'
        assert config.backup_enabled == False


class TestAlertConfig:
    """Testes da configuração de alertas."""
    
    def test_default_alert_config(self):
        """Testa a configuração padrão de alertas."""
        config = AlertConfig()
        assert config.enabled == True
        assert config.threshold_percent == 5.0
        assert config.check_interval_hours == 1
    
    def test_custom_alert_config(self, monkeypatch):
        """Testa configuração personalizada de alertas."""
        monkeypatch.setenv('ALERT_ENABLED', 'false')
        monkeypatch.setenv('ALERT_THRESHOLD_PERCENT', '10.0')
        
        config = AlertConfig()
        assert config.enabled == False
        assert config.threshold_percent == 10.0


class TestChartConfig:
    """Testes da configuração de gráficos."""
    
    def test_default_chart_config(self):
        """Testa a configuração padrão de gráficos."""
        config = ChartConfig()
        assert config.enabled == True
        assert config.width == 12
        assert config.height == 6
        assert config.dpi == 100
    
    def test_custom_chart_config(self, monkeypatch):
        """Testa configuração personalizada de gráficos."""
        monkeypatch.setenv('CHART_ENABLED', 'false')
        monkeypatch.setenv('CHART_WIDTH', '16')
        monkeypatch.setenv('CHART_HEIGHT', '8')
        
        config = ChartConfig()
        assert config.enabled == False
        assert config.width == 16
        assert config.height == 8


class TestConfig:
    """Testes da configuração principal."""
    
    def test_default_config(self):
        """Testa a configuração padrão."""
        config = Config()
        assert 'Mozilla' in config.user_agent
        assert config.webdriver is not None
        assert config.telegram is not None
        assert config.database is not None
        assert config.alert is not None
        assert config.chart is not None
