"""
Módulo de geração de gráficos.

Fornece funcionalidades para gerar gráficos de histórico
de Market Cap de criptomoedas.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
from datetime import datetime
from typing import Optional, List

import pandas as pd

from .config import config
from .logger import get_logger

logger = get_logger(__name__)


class ChartGenerator:
    """Gerenciador de geração de gráficos."""
    
    def __init__(self):
        """Inicializa o gerador de gráficos."""
        self.logger = logger
        self.output_dir = Path(config.chart.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Configurações do matplotlib
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def generate_market_cap_chart(
        self, 
        df: pd.DataFrame, 
        output_path: Optional[str] = None
    ) -> Optional[str]:
        """
        Gera um gráfico de histórico de Market Cap.
        
        Args:
            df: DataFrame com os dados das criptomoedas
            output_path: Caminho de saída do gráfico (opcional)
            
        Returns:
            Caminho do gráfico gerado ou None
        """
        if df.empty:
            self.logger.warning("⚠️ DataFrame vazio. Não é possível gerar gráfico.")
            return None
        
        try:
            # Converte timestamp para datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Converte market_cap para float
            df['market_cap_float'] = df['market_cap'].str.replace('US$', '').str.replace(',', '').astype(float)
            
            # Cria a figura
            fig, ax = plt.subplots(figsize=(config.chart.width, config.chart.height))
            dpi = config.chart.dpi
            
            # Plota cada criptomoeda
            for name in df['name'].unique():
                crypto_data = df[df['name'] == name].sort_values('timestamp')
                ax.plot(
                    crypto_data['timestamp'], 
                    crypto_data['market_cap_float'], 
                    marker='o', 
                    label=name,
                    linewidth=2,
                    markersize=4
                )
            
            # Configurações do gráfico
            ax.set_title('Histórico de Market Cap das Criptomoedas', fontsize=14, fontweight='bold')
            ax.set_xlabel('Data', fontsize=12)
            ax.set_ylabel('Market Cap (USD)', fontsize=12)
            ax.legend(loc='best', fontsize=10)
            ax.grid(True, alpha=0.3)
            
            # Formatação do eixo X
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M'))
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))
            plt.xticks(rotation=45)
            
            # Formatação do eixo Y
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
            
            # Ajusta layout
            plt.tight_layout()
            
            # Salva o gráfico
            if not output_path:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_path = self.output_dir / f"market_cap_history_{timestamp}.png"
            else:
                output_path = Path(output_path)
            
            plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"✅ Gráfico gerado: {output_path}")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao gerar gráfico: {e}")
            return None
    
    def generate_crypto_comparison_chart(
        self, 
        df: pd.DataFrame, 
        output_path: Optional[str] = None
    ) -> Optional[str]:
        """
        Gera um gráfico de comparação entre criptomoedas.
        
        Args:
            df: DataFrame com os dados das criptomoedas
            output_path: Caminho de saída do gráfico (opcional)
            
        Returns:
            Caminho do gráfico gerado ou None
        """
        if df.empty:
            self.logger.warning("⚠️ DataFrame vazio. Não é possível gerar gráfico.")
            return None
        
        try:
            # Converte market_cap para float
            df['market_cap_float'] = df['market_cap'].str.replace('US$', '').str.replace(',', '').astype(float)
            
            # Pega os dados mais recentes de cada criptomoeda
            latest_data = df.groupby('name').last().reset_index()
            
            # Ordena por market cap
            latest_data = latest_data.sort_values('market_cap_float', ascending=True)
            
            # Cria a figura
            fig, ax = plt.subplots(figsize=(config.chart.width, config.chart.height))
            dpi = config.chart.dpi
            
            # Plota gráfico de barras horizontal
            bars = ax.barh(
                latest_data['name'], 
                latest_data['market_cap_float'],
                color='steelblue'
            )
            
            # Adiciona valores nas barras
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax.text(
                    width, 
                    bar.get_y() + bar.get_height()/2, 
                    f'${width:,.0f}',
                    ha='left', 
                    va='center',
                    fontsize=10
                )
            
            # Configurações do gráfico
            ax.set_title('Comparação de Market Cap', fontsize=14, fontweight='bold')
            ax.set_xlabel('Market Cap (USD)', fontsize=12)
            ax.grid(True, alpha=0.3, axis='x')
            
            # Ajusta layout
            plt.tight_layout()
            
            # Salva o gráfico
            if not output_path:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_path = self.output_dir / f"crypto_comparison_{timestamp}.png"
            else:
                output_path = Path(output_path)
            
            plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"✅ Gráfico de comparação gerado: {output_path}")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao gerar gráfico de comparação: {e}")
            return None
    
    def generate_variation_chart(
        self, 
        df: pd.DataFrame, 
        output_path: Optional[str] = None
    ) -> Optional[str]:
        """
        Gera um gráfico de variação de criptomoedas.
        
        Args:
            df: DataFrame com os dados das criptomoedas
            output_path: Caminho de saída do gráfico (opcional)
            
        Returns:
            Caminho do gráfico gerado ou None
        """
        if df.empty:
            self.logger.warning("⚠️ DataFrame vazio. Não é possível gerar gráfico.")
            return None
        
        try:
            # Converte timestamp para datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Converte market_cap para float
            df['market_cap_float'] = df['market_cap'].str.replace('US$', '').str.replace(',', '').astype(float)
            
            # Calcula variação percentual
            df['variation'] = df.groupby('name')['market_cap_float'].pct_change() * 100
            
            # Remove valores nulos
            df = df.dropna(subset=['variation'])
            
            if df.empty:
                self.logger.warning("⚠️ Não há dados suficientes para calcular variação.")
                return None
            
            # Cria a figura
            fig, ax = plt.subplots(figsize=(config.chart.width, config.chart.height))
            dpi = config.chart.dpi
            
            # Plota cada criptomoeda
            for name in df['name'].unique():
                crypto_data = df[df['name'] == name].sort_values('timestamp')
                color = 'green' if crypto_data['variation'].iloc[-1] >= 0 else 'red'
                ax.plot(
                    crypto_data['timestamp'], 
                    crypto_data['variation'], 
                    marker='o', 
                    label=name,
                    color=color,
                    linewidth=2,
                    markersize=4
                )
            
            # Configurações do gráfico
            ax.set_title('Variação de Market Cap (%)', fontsize=14, fontweight='bold')
            ax.set_xlabel('Data', fontsize=12)
            ax.set_ylabel('Variação (%)', fontsize=12)
            ax.legend(loc='best', fontsize=10)
            ax.grid(True, alpha=0.3)
            ax.axhline(y=0, color='black', linestyle='--', linewidth=1)
            
            # Formatação do eixo X
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M'))
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))
            plt.xticks(rotation=45)
            
            # Ajusta layout
            plt.tight_layout()
            
            # Salva o gráfico
            if not output_path:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_path = self.output_dir / f"variation_chart_{timestamp}.png"
            else:
                output_path = Path(output_path)
            
            plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"✅ Gráfico de variação gerado: {output_path}")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao gerar gráfico de variação: {e}")
            return None
    
    def cleanup_old_charts(self, days: int = 7) -> int:
        """
        Remove gráficos antigos.
        
        Args:
            days: Número de dias para manter
            
        Returns:
            Número de gráficos removidos
        """
        try:
            from datetime import timedelta
            
            cutoff_time = datetime.now() - timedelta(days=days)
            removed_count = 0
            
            for chart_file in self.output_dir.glob('*.png'):
                if chart_file.stat().st_mtime < cutoff_time.timestamp():
                    chart_file.unlink()
                    removed_count += 1
            
            if removed_count > 0:
                self.logger.info(f"✅ {removed_count} gráficos antigos removidos")
            
            return removed_count
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao limpar gráficos antigos: {e}")
            return 0
