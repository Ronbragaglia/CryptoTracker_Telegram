"""
Módulo principal de rastreamento de criptomoedas.

Fornece a classe CryptoTracker que implementa toda a lógica de
coleta, armazenamento e alerta de criptomoedas.
"""

import time
from typing import List, Dict, Any, Optional
from datetime import datetime

import pandas as pd
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .config import config
from .logger import get_logger
from .telegram import TelegramNotifier
from .database import DatabaseManager
from .chart import ChartGenerator

logger = get_logger(__name__)


class CryptoTracker:
    """Classe principal para rastreamento de criptomoedas."""
    
    def __init__(self):
        """Inicializa o rastreador de criptomoedas."""
        self.logger = logger
        self.driver = None
        self.telegram = TelegramNotifier()
        self.database = DatabaseManager()
        self.chart_generator = ChartGenerator()
        self._setup_driver()
    
    def _setup_driver(self) -> None:
        """
        Configura e inicializa o driver do Selenium.
        
        Raises:
            Exception: Se houver erro ao configurar o driver
        """
        try:
            options = Options()
            
            # Configurações básicas
            options.add_argument("--headless") if config.webdriver.headless else None
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument(f"user-agent={config.user_agent}")
            
            # Configurações de proxy
            if config.proxy.is_configured:
                options.add_argument(f"--proxy-server={config.proxy.proxy_string}")
                self.logger.info(f"Usando proxy: {config.proxy.proxy_string}")
            
            # Inicializa o driver
            self.driver = uc.Chrome(options=options)
            self.driver.set_page_load_timeout(config.webdriver.page_load_timeout)
            
            self.logger.info("✅ Driver do Selenium configurado com sucesso")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao configurar driver: {e}")
            raise
    
    def _wait_for_element(
        self, 
        by: By, 
        value: str, 
        timeout: Optional[int] = None
    ) -> Any:
        """
        Aguarda até que um elemento esteja presente na página.
        
        Args:
            by: Método de localização (By.CSS_SELECTOR, By.XPATH, etc.)
            value: Valor do localizador
            timeout: Tempo máximo de espera em segundos
            
        Returns:
            Elemento encontrado
            
        Raises:
            TimeoutException: Se o elemento não for encontrado
        """
        timeout = timeout or config.webdriver.element_wait_timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))
    
    def collect_crypto_data(self) -> List[Dict[str, Any]]:
        """
        Coleta dados de criptomoedas do CoinGecko.
        
        Returns:
            Lista de dicionários com dados das criptomoedas
        """
        try:
            self.logger.info("🔄 Buscando dados de criptomoedas...")
            
            # Acessa o CoinGecko
            self.driver.get(config.scraping.coingecko_url)
            time.sleep(config.webdriver.scroll_delay)
            
            # Encontra as linhas da tabela
            rows = self.driver.find_elements(By.XPATH, "//tbody/tr")[:config.scraping.max_cryptos]
            
            crypto_data = []
            
            for i, row in enumerate(rows, start=1):
                try:
                    # Extrai dados da linha
                    name = row.find_element(By.XPATH, ".//td[3]//a").text
                    market_cap = row.find_element(By.XPATH, ".//td[10]").text
                    
                    # Tenta extrair dados adicionais
                    try:
                        price = row.find_element(By.XPATH, ".//td[4]").text
                    except:
                        price = None
                    
                    try:
                        volume_24h = row.find_element(By.XPATH, ".//td[8]").text
                    except:
                        volume_24h = None
                    
                    try:
                        change_24h = row.find_element(By.XPATH, ".//td[6]").text
                    except:
                        change_24h = None
                    
                    crypto_data.append({
                        'name': name,
                        'market_cap': market_cap,
                        'price': price,
                        'volume_24h': volume_24h,
                        'change_24h': change_24h
                    })
                    
                except Exception as e:
                    self.logger.warning(f"⚠️ Erro ao coletar dados da moeda {i}: {e}")
                    continue
            
            self.logger.info(f"✅ Dados coletados: {len(crypto_data)} criptomoedas")
            
            # Armazena no banco de dados
            if crypto_data:
                self.database.insert_crypto_data(crypto_data)
            
            # Envia atualização para o Telegram
            if crypto_data:
                self.telegram.send_crypto_update(crypto_data)
            
            return crypto_data
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao coletar dados: {e}")
            return []
    
    def check_alerts(self) -> List[str]:
        """
        Verifica se há alertas de variação a serem enviados.
        
        Returns:
            Lista de alertas enviados
        """
        if not config.alert.enabled:
            return []
        
        try:
            self.logger.info("🔍 Verificando alertas de variação...")
            
            alerts_sent = []
            crypto_names = self.database.get_all_crypto_names()
            
            for name in crypto_names:
                variation = self.database.get_crypto_variation(name, hours=24)
                
                if variation is None:
                    continue
                
                if abs(variation) >= config.alert.threshold_percent:
                    self.telegram.send_alert(name, variation)
                    alerts_sent.append(f"{name}: {variation:.2f}%")
            
            if alerts_sent:
                self.logger.info(f"✅ {len(alerts_sent)} alertas enviados")
            else:
                self.logger.info("✅ Nenhum alerta para enviar")
            
            return alerts_sent
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao verificar alertas: {e}")
            return []
    
    def generate_charts(self) -> Optional[str]:
        """
        Gera gráficos do histórico de criptomoedas.
        
        Returns:
            Caminho do gráfico gerado ou None
        """
        if not config.chart.enabled:
            return None
        
        try:
            self.logger.info("📊 Gerando gráficos...")
            
            # Recupera dados do banco de dados
            df = self.database.get_crypto_history(limit=200)
            
            if df.empty:
                self.logger.warning("⚠️ Sem dados suficientes para gerar gráficos")
                return None
            
            # Gera gráfico de histórico
            chart_path = self.chart_generator.generate_market_cap_chart(df)
            
            # Envia gráfico para o Telegram
            if chart_path:
                self.telegram.send_chart(chart_path)
            
            return chart_path
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao gerar gráficos: {e}")
            return None
    
    def run_once(self) -> None:
        """Executa uma única vez: coleta dados, verifica alertas e gera gráficos."""
        self.collect_crypto_data()
        self.check_alerts()
        self.generate_charts()
    
    def start_scheduled(self) -> None:
        """
        Inicia o rastreador com agendamento automático.
        
        Usa a biblioteca schedule para executar tarefas em intervalos configurados.
        """
        import schedule
        
        self.logger.info("=" * 80)
        self.logger.info("🚀 Iniciando o Crypto Tracker com agendamento automático")
        self.logger.info("=" * 80)
        
        # Configura agendamento
        schedule.every(config.schedule.data_collection_interval_hours).hours.do(self.collect_crypto_data)
        schedule.every(config.schedule.alert_check_interval_hours).hours.do(self.check_alerts)
        schedule.every(config.schedule.chart_generation_interval_hours).hours.do(self.generate_charts)
        
        self.logger.info(f"📅 Coleta de dados: a cada {config.schedule.data_collection_interval_hours} horas")
        self.logger.info(f"📅 Verificação de alertas: a cada {config.schedule.alert_check_interval_hours} horas")
        self.logger.info(f"📅 Geração de gráficos: a cada {config.schedule.chart_generation_interval_hours} horas")
        
        # Testa conexão com Telegram
        self.telegram.test_connection()
        
        # Loop principal
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Verifica a cada minuto
                
        except KeyboardInterrupt:
            self.logger.info("\n⚠️ Operação interrompida pelo usuário")
        except Exception as e:
            self.logger.error(f"❌ Erro no loop principal: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self) -> None:
        """Limpa recursos e fecha conexões."""
        try:
            if self.driver:
                self.driver.quit()
                self.logger.info("✅ Driver fechado")
            
            self.logger.info("✅ Crypto Tracker encerrado")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao limpar recursos: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """
        Retorna o status atual do rastreador.
        
        Returns:
            Dicionário com informações de status
        """
        return {
            'database_path': config.database.path,
            'record_count': self.database.get_record_count(),
            'database_size': self.database.get_database_size(),
            'crypto_count': len(self.database.get_all_crypto_names()),
            'telegram_configured': config.telegram.is_configured,
            'alert_enabled': config.alert.enabled,
            'chart_enabled': config.chart.enabled
        }
