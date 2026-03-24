"""
Interface de linha de comando do Crypto Tracker.

Fornece uma CLI para executar o rastreador com diferentes opções.
"""

import argparse
import sys

from .tracker import CryptoTracker
from .config import config
from .logger import get_logger, Logger

logger = get_logger(__name__)


def create_parser() -> argparse.ArgumentParser:
    """
    Cria o parser de argumentos da CLI.
    
    Returns:
        Parser configurado
    """
    parser = argparse.ArgumentParser(
        description='Crypto Tracker Telegram - Monitoramento automático de criptomoedas',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  # Executa o rastreador uma vez
  python -m crypto_tracker --once
  
  # Executa o rastreador com agendamento automático
  python -m crypto_tracker --scheduled
  
  # Executa em modo verbose
  python -m crypto_tracker --scheduled --verbose
  
  # Coleta dados de 20 criptomoedas
  python -m crypto_tracker --once --max-cryptos 20
  
  # Mostra status do rastreador
  python -m crypto_tracker --status
        """
    )
    
    parser.add_argument(
        '--once',
        action='store_true',
        help='Executa o rastreador apenas uma vez'
    )
    
    parser.add_argument(
        '--scheduled',
        action='store_true',
        help='Executa o rastreador com agendamento automático'
    )
    
    parser.add_argument(
        '--max-cryptos',
        type=int,
        default=None,
        help='Número máximo de criptomoedas para coletar (padrão: 10)'
    )
    
    parser.add_argument(
        '--no-alerts',
        action='store_true',
        help='Desabilita alertas de variação'
    )
    
    parser.add_argument(
        '--no-charts',
        action='store_true',
        help='Desabilita geração de gráficos'
    )
    
    parser.add_argument(
        '--status',
        action='store_true',
        help='Mostra o status atual do rastreador'
    )
    
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Modo verbose (mostra mais detalhes)'
    )
    
    parser.add_argument(
        '--quiet',
        '-q',
        action='store_true',
        help='Modo silencioso (mostra apenas erros)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 2.0.0'
    )
    
    return parser


def main(args: argparse.Namespace = None) -> int:
    """
    Função principal da CLI.
    
    Args:
        args: Argumentos da linha de comando
        
    Returns:
        Código de saída (0 para sucesso, 1 para erro)
    """
    parser = create_parser()
    args = args or parser.parse_args()
    
    # Configura nível de log
    if args.verbose:
        Logger.set_level('DEBUG')
    elif args.quiet:
        Logger.set_level('ERROR')
    
    try:
        # Atualiza configurações baseadas nos argumentos
        if args.max_cryptos:
            config.scraping.max_cryptos = args.max_cryptos
        
        if args.no_alerts:
            config.alert.enabled = False
        
        if args.no_charts:
            config.chart.enabled = False
        
        # Cria instância do rastreador
        tracker = CryptoTracker()
        
        # Mostra status se solicitado
        if args.status:
            status = tracker.get_status()
            print("\n📊 Status do Crypto Tracker")
            print("=" * 80)
            print(f"📁 Banco de dados: {status['database_path']}")
            print(f"📝 Registros: {status['record_count']}")
            print(f"💾 Tamanho: {status['database_size']} bytes")
            print(f"🪙 Criptomoedas: {status['crypto_count']}")
            print(f"📱 Telegram configurado: {status['telegram_configured']}")
            print(f"🔔 Alertas habilitados: {status['alert_enabled']}")
            print(f"📊 Gráficos habilitados: {status['chart_enabled']}")
            print("=" * 80)
            return 0
        
        # Executa rastreador
        if args.once:
            logger.info("🔄 Executando rastreador uma vez...")
            tracker.run_once()
            logger.info("✅ Rastreador concluído")
        elif args.scheduled:
            tracker.start_scheduled()
        else:
            # Se nenhum modo for especificado, executa uma vez
            logger.info("🔄 Executando rastreador uma vez...")
            tracker.run_once()
            logger.info("✅ Rastreador concluído")
            print("\n💡 Dica: Use --scheduled para executar com agendamento automático")
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("\n⚠️ Operação cancelada pelo usuário")
        return 1
        
    except Exception as e:
        logger.error(f"❌ Erro: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
