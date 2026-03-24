"""
Módulo de configuração do Crypto Tracker Telegram.

Gerencia todas as configurações do sistema, incluindo variáveis de ambiente,
timeout, proxy e outras opções de configuração.
"""

import os
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path

from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()


@dataclass
class TelegramConfig:
    """Configurações do Telegram Bot."""
    bot_token: str = field(default_factory=lambda: os.getenv("TELEGRAM_BOT_TOKEN", ""))
    chat_id: str = field(default_factory=lambda: os.getenv("TELEGRAM_CHAT_ID", ""))
    
    @property
    def is_configured(self) -> bool:
        """Verifica se o Telegram está configurado."""
        return bool(self.bot_token and self.chat_id)
    
    def validate(self) -> None:
        """Valida as configurações do Telegram."""
        if not self.is_configured:
            raise ValueError(
                "❌ ERRO: Token ou Chat ID do Telegram não foram configurados!\n"
                "Por favor, configure TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID no arquivo .env"
            )


@dataclass
class WebDriverConfig:
    """Configurações do WebDriver."""
    browser: str = field(default_factory=lambda: os.getenv("WEBDRIVER_BROWSER", "chrome"))
    headless: bool = field(default_factory=lambda: os.getenv("WEBDRIVER_HEADLESS", "true").lower() == "true")
    page_load_timeout: int = field(default_factory=lambda: int(os.getenv("PAGE_LOAD_TIMEOUT", "30")))
    element_wait_timeout: int = field(default_factory=lambda: int(os.getenv("ELEMENT_WAIT_TIMEOUT", "10")))
    scroll_delay: float = field(default_factory=lambda: float(os.getenv("SCROLL_DELAY", "2")))


@dataclass
class ScrapingConfig:
    """Configurações de scraping."""
    max_cryptos: int = field(default_factory=lambda: int(os.getenv("MAX_CRYPTOS", "10")))
    coingecko_url: str = field(default_factory=lambda: os.getenv("COINGECKO_URL", "https://www.coingecko.com/pt"))
    coingecko_api: str = field(default_factory=lambda: os.getenv("COINGECKO_API", "https://api.coingecko.com/api/v3"))


@dataclass
class DatabaseConfig:
    """Configurações do banco de dados."""
    path: str = field(default_factory=lambda: os.getenv("DATABASE_PATH", "data/crypto_data.db"))
    backup_enabled: bool = field(default_factory=lambda: os.getenv("DATABASE_BACKUP_ENABLED", "true").lower() == "true")
    backup_interval_hours: int = field(default_factory=lambda: int(os.getenv("DATABASE_BACKUP_INTERVAL_HOURS", "24")))
    
    def __post_init__(self):
        """Garante que o diretório do banco de dados existe."""
        db_path = Path(self.path)
        db_path.parent.mkdir(parents=True, exist_ok=True)


@dataclass
class AlertConfig:
    """Configurações de alertas."""
    enabled: bool = field(default_factory=lambda: os.getenv("ALERT_ENABLED", "true").lower() == "true")
    threshold_percent: float = field(default_factory=lambda: float(os.getenv("ALERT_THRESHOLD_PERCENT", "5.0")))
    check_interval_hours: int = field(default_factory=lambda: int(os.getenv("ALERT_CHECK_INTERVAL_HOURS", "1")))


@dataclass
class ChartConfig:
    """Configurações de gráficos."""
    enabled: bool = field(default_factory=lambda: os.getenv("CHART_ENABLED", "true").lower() == "true")
    generation_interval_hours: int = field(default_factory=lambda: int(os.getenv("CHART_GENERATION_INTERVAL_HOURS", "6")))
    width: int = field(default_factory=lambda: int(os.getenv("CHART_WIDTH", "12")))
    height: int = field(default_factory=lambda: int(os.getenv("CHART_HEIGHT", "6")))
    dpi: int = field(default_factory=lambda: int(os.getenv("CHART_DPI", "100")))
    output_dir: str = field(default_factory=lambda: os.getenv("CHART_OUTPUT_DIR", "data/charts"))
    
    def __post_init__(self):
        """Garante que o diretório de saída dos gráficos existe."""
        chart_path = Path(self.output_dir)
        chart_path.mkdir(parents=True, exist_ok=True)


@dataclass
class ScheduleConfig:
    """Configurações de agendamento."""
    data_collection_interval_hours: int = field(default_factory=lambda: int(os.getenv("DATA_COLLECTION_INTERVAL_HOURS", "2")))
    chart_generation_interval_hours: int = field(default_factory=lambda: int(os.getenv("CHART_GENERATION_INTERVAL_HOURS", "6")))
    alert_check_interval_hours: int = field(default_factory=lambda: int(os.getenv("ALERT_CHECK_INTERVAL_HOURS", "1")))


@dataclass
class LogConfig:
    """Configurações de logging."""
    level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    file: str = field(default_factory=lambda: os.getenv("LOG_FILE", "logs/crypto_tracker.log"))
    format: str = field(default_factory=lambda: os.getenv(
        "LOG_FORMAT",
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))
    
    def __post_init__(self):
        """Garante que o diretório de logs existe."""
        log_path = Path(self.file)
        log_path.parent.mkdir(parents=True, exist_ok=True)


@dataclass
class OutputConfig:
    """Configurações de saída."""
    dir: str = field(default_factory=lambda: os.getenv("OUTPUT_DIR", "data"))
    backup_dir: str = field(default_factory=lambda: os.getenv("BACKUP_DIR", "data/backups"))
    
    def __post_init__(self):
        """Garante que os diretórios de saída existem."""
        output_path = Path(self.dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        backup_path = Path(self.backup_dir)
        backup_path.mkdir(parents=True, exist_ok=True)


@dataclass
class ProxyConfig:
    """Configurações de proxy."""
    enabled: bool = field(default_factory=lambda: os.getenv("PROXY_ENABLED", "false").lower() == "true")
    host: Optional[str] = field(default_factory=lambda: os.getenv("PROXY_HOST"))
    port: Optional[int] = field(default_factory=lambda: int(os.getenv("PROXY_PORT", "0")) if os.getenv("PROXY_PORT") else None)
    username: Optional[str] = field(default_factory=lambda: os.getenv("PROXY_USERNAME"))
    password: Optional[str] = field(default_factory=lambda: os.getenv("PROXY_PASSWORD"))
    
    @property
    def is_configured(self) -> bool:
        """Verifica se o proxy está configurado."""
        return self.enabled and bool(self.host and self.port)
    
    @property
    def proxy_string(self) -> str:
        """Retorna a string de conexão do proxy."""
        if not self.is_configured:
            return ""
        
        if self.username and self.password:
            return f"http://{self.username}:{self.password}@{self.host}:{self.port}"
        return f"http://{self.host}:{self.port}"


@dataclass
class RateLimitingConfig:
    """Configurações de rate limiting."""
    request_delay_seconds: float = field(default_factory=lambda: float(os.getenv("REQUEST_DELAY_SECONDS", "2")))
    max_retries: int = field(default_factory=lambda: int(os.getenv("MAX_RETRIES", "3")))
    retry_delay_seconds: float = field(default_factory=lambda: float(os.getenv("RETRY_DELAY_SECONDS", "5")))


@dataclass
class NotificationConfig:
    """Configurações de notificações."""
    enabled: bool = field(default_factory=lambda: os.getenv("NOTIFICATION_ENABLED", "true").lower() == "true")
    format: str = field(default_factory=lambda: os.getenv("NOTIFICATION_FORMAT", "markdown"))
    parse_mode: str = field(default_factory=lambda: os.getenv("NOTIFICATION_PARSE_MODE", "MarkdownV2"))


@dataclass
class Config:
    """Configuração principal do Crypto Tracker."""
    user_agent: str = field(default_factory=lambda: os.getenv(
        "USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ))
    
    telegram: TelegramConfig = field(default_factory=TelegramConfig)
    webdriver: WebDriverConfig = field(default_factory=WebDriverConfig)
    scraping: ScrapingConfig = field(default_factory=ScrapingConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    alert: AlertConfig = field(default_factory=AlertConfig)
    chart: ChartConfig = field(default_factory=ChartConfig)
    schedule: ScheduleConfig = field(default_factory=ScheduleConfig)
    log: LogConfig = field(default_factory=LogConfig)
    output: OutputConfig = field(default_factory=OutputConfig)
    proxy: ProxyConfig = field(default_factory=ProxyConfig)
    rate_limiting: RateLimitingConfig = field(default_factory=RateLimitingConfig)
    notification: NotificationConfig = field(default_factory=NotificationConfig)
    
    def __post_init__(self):
        """Valida as configurações após a inicialização."""
        self.telegram.validate()


# Configuração global
config = Config()
