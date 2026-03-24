"""
Módulo de gerenciamento de banco de dados.

Fornece funcionalidades para armazenar e recuperar dados
de criptomoedas em SQLite.
"""

import sqlite3
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from contextlib import contextmanager

import pandas as pd

from .config import config
from .logger import get_logger

logger = get_logger(__name__)


class DatabaseManager:
    """Gerenciador do banco de dados SQLite."""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Inicializa o gerenciador do banco de dados.
        
        Args:
            db_path: Caminho do banco de dados (opcional)
        """
        self.logger = logger
        self.db_path = db_path or config.database.path
        self._ensure_database_exists()
    
    @contextmanager
    def _get_connection(self):
        """
        Context manager para conexão com o banco de dados.
        
        Yields:
            Conexão com o banco de dados
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Erro no banco de dados: {e}")
            raise
        finally:
            conn.close()
    
    def _ensure_database_exists(self) -> None:
        """Garante que o banco de dados e as tabelas existem."""
        db_path = Path(self.db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabela de criptomoedas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cryptos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    name TEXT NOT NULL,
                    market_cap TEXT NOT NULL,
                    price TEXT,
                    volume_24h TEXT,
                    change_24h TEXT
                )
            """)
            
            # Índices para melhorar performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON cryptos(timestamp)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_name 
                ON cryptos(name)
            """)
            
            self.logger.info("✅ Banco de dados inicializado com sucesso")
    
    def insert_crypto_data(self, crypto_data: List[Dict[str, Any]]) -> bool:
        """
        Insere dados de criptomoedas no banco de dados.
        
        Args:
            crypto_data: Lista de dicionários com dados das criptomoedas
            
        Returns:
            True se a inserção foi bem-sucedida, False caso contrário
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                for crypto in crypto_data:
                    cursor.execute("""
                        INSERT INTO cryptos (timestamp, name, market_cap, price, volume_24h, change_24h)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        timestamp,
                        crypto.get('name'),
                        crypto.get('market_cap'),
                        crypto.get('price'),
                        crypto.get('volume_24h'),
                        crypto.get('change_24h')
                    ))
                
                self.logger.info(f"✅ {len(crypto_data)} registros inseridos no banco de dados")
                return True
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao inserir dados no banco de dados: {e}")
            return False
    
    def get_crypto_history(
        self, 
        name: Optional[str] = None, 
        limit: int = 100
    ) -> pd.DataFrame:
        """
        Recupera o histórico de criptomoedas do banco de dados.
        
        Args:
            name: Nome da criptomoeda (opcional)
            limit: Número máximo de registros
            
        Returns:
            DataFrame com o histórico
        """
        try:
            with self._get_connection() as conn:
                if name:
                    query = """
                        SELECT * FROM cryptos 
                        WHERE name = ? 
                        ORDER BY timestamp DESC 
                        LIMIT ?
                    """
                    params = (name, limit)
                else:
                    query = """
                        SELECT * FROM cryptos 
                        ORDER BY timestamp DESC 
                        LIMIT ?
                    """
                    params = (limit,)
                
                df = pd.read_sql_query(query, conn, params=params)
                self.logger.info(f"✅ {len(df)} registros recuperados do banco de dados")
                return df
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao recuperar dados do banco de dados: {e}")
            return pd.DataFrame()
    
    def get_latest_crypto_data(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Recupera os dados mais recentes de uma criptomoeda.
        
        Args:
            name: Nome da criptomoeda
            
        Returns:
            Dicionário com os dados mais recentes ou None
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM cryptos 
                    WHERE name = ? 
                    ORDER BY timestamp DESC 
                    LIMIT 1
                """, (name,))
                
                row = cursor.fetchone()
                if row:
                    return dict(row)
                return None
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao recuperar dados mais recentes: {e}")
            return None
    
    def get_crypto_variation(
        self, 
        name: str, 
        hours: int = 24
    ) -> Optional[float]:
        """
        Calcula a variação de uma criptomoeda em um período.
        
        Args:
            name: Nome da criptomoeda
            hours: Período em horas
            
        Returns:
            Variação em percentual ou None
        """
        try:
            df = self.get_crypto_history(name, limit=100)
            
            if df.empty or len(df) < 2:
                return None
            
            # Converte market_cap para float
            df['market_cap_float'] = df['market_cap'].str.replace('US$', '').str.replace(',', '').astype(float)
            
            # Pega o valor mais recente e o valor mais antigo no período
            latest = df.iloc[0]['market_cap_float']
            oldest = df.iloc[-1]['market_cap_float']
            
            if oldest == 0:
                return None
            
            variation = ((latest - oldest) / oldest) * 100
            return variation
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao calcular variação: {e}")
            return None
    
    def get_all_crypto_names(self) -> List[str]:
        """
        Recupera todos os nomes de criptomoedas no banco de dados.
        
        Returns:
            Lista de nomes de criptomoedas
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT DISTINCT name FROM cryptos 
                    ORDER BY name
                """)
                
                names = [row[0] for row in cursor.fetchall()]
                return names
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao recuperar nomes de criptomoedas: {e}")
            return []
    
    def cleanup_old_data(self, days: int = 30) -> int:
        """
        Remove dados antigos do banco de dados.
        
        Args:
            days: Número de dias para manter
            
        Returns:
            Número de registros removidos
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM cryptos 
                    WHERE timestamp < datetime('now', '-' || ? || ' days')
                """, (days,))
                
                deleted_count = cursor.rowcount
                self.logger.info(f"✅ {deleted_count} registros antigos removidos")
                return deleted_count
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao limpar dados antigos: {e}")
            return 0
    
    def backup_database(self, backup_path: Optional[str] = None) -> bool:
        """
        Faz um backup do banco de dados.
        
        Args:
            backup_path: Caminho para o backup (opcional)
            
        Returns:
            True se o backup foi bem-sucedido, False caso contrário
        """
        if not config.database.backup_enabled:
            self.logger.debug("Backup desabilitado")
            return False
        
        try:
            if not backup_path:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_path = f"{config.output.backup_dir}/crypto_data_{timestamp}.db"
            
            shutil.copy2(self.db_path, backup_path)
            self.logger.info(f"✅ Backup criado: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao criar backup: {e}")
            return False
    
    def get_database_size(self) -> int:
        """
        Retorna o tamanho do banco de dados em bytes.
        
        Returns:
            Tamanho do banco de dados em bytes
        """
        try:
            return Path(self.db_path).stat().st_size
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter tamanho do banco de dados: {e}")
            return 0
    
    def get_record_count(self) -> int:
        """
        Retorna o número de registros no banco de dados.
        
        Returns:
            Número de registros
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM cryptos")
                count = cursor.fetchone()[0]
                return count
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao contar registros: {e}")
            return 0
