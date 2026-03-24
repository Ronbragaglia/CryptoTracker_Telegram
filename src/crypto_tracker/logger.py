"""
Módulo de logging do Crypto Tracker Telegram.

Fornece uma interface unificada para logging em toda a aplicação.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

from .config import config


class Logger:
    """Gerenciador de logs centralizado."""
    
    _loggers: dict = {}
    
    @classmethod
    def get_logger(cls, name: str = __name__) -> logging.Logger:
        """
        Obtém ou cria um logger com o nome especificado.
        
        Args:
            name: Nome do logger (geralmente __name__ do módulo)
            
        Returns:
            Logger configurado
        """
        if name not in cls._loggers:
            cls._loggers[name] = cls._setup_logger(name)
        return cls._loggers[name]
    
    @classmethod
    def _setup_logger(cls, name: str) -> logging.Logger:
        """
        Configura um logger com handlers de console e arquivo.
        
        Args:
            name: Nome do logger
            
        Returns:
            Logger configurado
        """
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, config.log.level))
        
        # Remove handlers existentes para evitar duplicação
        logger.handlers.clear()
        
        # Formato do log
        formatter = logging.Formatter(config.log.format)
        
        # Handler de console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Handler de arquivo
        log_file = Path(config.log.file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(getattr(logging, config.log.level))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Evita propagação para loggers pai
        logger.propagate = False
        
        return logger
    
    @classmethod
    def set_level(cls, level: str) -> None:
        """
        Define o nível de log para todos os loggers.
        
        Args:
            level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        log_level = getattr(logging, level.upper(), logging.INFO)
        for logger in cls._loggers.values():
            logger.setLevel(log_level)
            for handler in logger.handlers:
                handler.setLevel(log_level)


def get_logger(name: str = __name__) -> logging.Logger:
    """
    Função de conveniência para obter um logger.
    
    Args:
        name: Nome do logger
        
    Returns:
        Logger configurado
    """
    return Logger.get_logger(name)
