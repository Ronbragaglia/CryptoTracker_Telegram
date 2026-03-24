"""
Crypto Tracker Telegram - Monitoramento automático de criptomoedas

Este pacote fornece ferramentas para monitorar criptomoedas em tempo real
e enviar alertas automáticos via Telegram.
"""

__version__ = "2.0.0"
__author__ = "Rone Bragaglia"
__email__ = "rone.bragaglia@uni9.edu.br"

from .tracker import CryptoTracker
from .config import Config
from .telegram import TelegramNotifier
from .database import DatabaseManager
from .chart import ChartGenerator

__all__ = [
    "CryptoTracker",
    "Config",
    "TelegramNotifier",
    "DatabaseManager",
    "ChartGenerator",
]
