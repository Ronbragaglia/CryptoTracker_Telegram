"""
Módulo de notificações do Telegram.

Fornece funcionalidades para enviar mensagens e alertas
via Telegram Bot API.
"""

import requests
from typing import Optional, List
from pathlib import Path

from .config import config
from .logger import get_logger

logger = get_logger(__name__)


class TelegramNotifier:
    """Gerenciador de notificações via Telegram."""
    
    def __init__(self):
        """Inicializa o notificador do Telegram."""
        self.logger = logger
        self.bot_token = config.telegram.bot_token
        self.chat_id = config.telegram.chat_id
        self.parse_mode = config.notification.parse_mode
        
        # Valida as configurações
        config.telegram.validate()
        
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def send_message(
        self, 
        text: str, 
        parse_mode: Optional[str] = None,
        disable_web_page_preview: bool = False
    ) -> bool:
        """
        Envia uma mensagem de texto para o Telegram.
        
        Args:
            text: Texto da mensagem
            parse_mode: Modo de parse (Markdown, HTML, etc.)
            disable_web_page_preview: Desabilitar preview de links
            
        Returns:
            True se a mensagem foi enviada com sucesso, False caso contrário
        """
        if not config.notification.enabled:
            self.logger.debug("Notificações desabilitadas. Mensagem não enviada.")
            return False
        
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": parse_mode or self.parse_mode,
                "disable_web_page_preview": disable_web_page_preview
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            self.logger.info("✅ Mensagem enviada com sucesso para o Telegram")
            return True
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"❌ Erro ao enviar mensagem para o Telegram: {e}")
            return False
    
    def send_photo(
        self, 
        photo_path: str, 
        caption: Optional[str] = None
    ) -> bool:
        """
        Envia uma foto para o Telegram.
        
        Args:
            photo_path: Caminho da foto
            caption: Legenda da foto
            
        Returns:
            True se a foto foi enviada com sucesso, False caso contrário
        """
        if not config.notification.enabled:
            self.logger.debug("Notificações desabilitadas. Foto não enviada.")
            return False
        
        try:
            url = f"{self.base_url}/sendPhoto"
            
            with open(photo_path, 'rb') as photo:
                files = {"photo": photo}
                data = {"chat_id": self.chat_id}
                
                if caption:
                    data["caption"] = caption
                
                response = requests.post(url, files=files, data=data, timeout=30)
                response.raise_for_status()
            
            self.logger.info(f"✅ Foto enviada com sucesso: {photo_path}")
            return True
            
        except FileNotFoundError:
            self.logger.error(f"❌ Arquivo não encontrado: {photo_path}")
            return False
        except requests.exceptions.RequestException as e:
            self.logger.error(f"❌ Erro ao enviar foto para o Telegram: {e}")
            return False
    
    def send_crypto_update(self, cryptos: List[dict]) -> bool:
        """
        Envia uma atualização de criptomoedas formatada.
        
        Args:
            cryptos: Lista de dicionários com dados das criptomoedas
            
        Returns:
            True se a mensagem foi enviada com sucesso, False caso contrário
        """
        message = "📊 **Atualização das Criptomoedas:**\n\n"
        
        for crypto in cryptos:
            name = crypto.get('name', 'N/A')
            market_cap = crypto.get('market_cap', 'N/A')
            message += f"🔹 {name} - Market Cap: {market_cap}\n"
        
        return self.send_message(message)
    
    def send_alert(self, crypto_name: str, variation: float) -> bool:
        """
        Envia um alerta de variação de criptomoeda.
        
        Args:
            crypto_name: Nome da criptomoeda
            variation: Variação em percentual
            
        Returns:
            True se o alerta foi enviado com sucesso, False caso contrário
        """
        if not config.alert.enabled:
            return False
        
        emoji = "📈" if variation > 0 else "📉"
        message = f"{emoji} **Alerta de Variação**\n\n"
        message += f"⚠️ {crypto_name} teve uma variação de {variation:.2f}%!"
        
        return self.send_message(message)
    
    def send_chart(self, chart_path: str, caption: str = "📊 Histórico de Market Cap") -> bool:
        """
        Envia um gráfico para o Telegram.
        
        Args:
            chart_path: Caminho do gráfico
            caption: Legenda do gráfico
            
        Returns:
            True se o gráfico foi enviado com sucesso, False caso contrário
        """
        return self.send_photo(chart_path, caption)
    
    def test_connection(self) -> bool:
        """
        Testa a conexão com o Telegram Bot API.
        
        Returns:
            True se a conexão foi bem-sucedida, False caso contrário
        """
        try:
            url = f"{self.base_url}/getMe"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            bot_info = response.json()
            self.logger.info(f"✅ Conexão com Telegram estabelecida: {bot_info['result']['first_name']}")
            return True
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"❌ Erro ao conectar com Telegram: {e}")
            return False
