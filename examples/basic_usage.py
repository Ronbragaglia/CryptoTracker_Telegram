#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo básico de uso do Crypto Tracker Telegram.

Este exemplo demonstra como usar o Crypto Tracker para
monitorar criptomoedas e receber alertas no Telegram.
"""

from crypto_tracker import CryptoTracker


def main():
    """Função principal do exemplo."""
    print("=" * 80)
    print("🚀 Exemplo Básico do Crypto Tracker Telegram")
    print("=" * 80)
    
    # Cria instância do rastreador
    tracker = CryptoTracker()
    
    # Executa o rastreador uma vez
    print("\n📥 Coletando dados de criptomoedas...")
    tracker.run_once()
    
    # Mostra status
    print("\n📊 Status do Rastreador:")
    status = tracker.get_status()
    print(f"  📁 Banco de dados: {status['database_path']}")
    print(f"  📝 Registros: {status['record_count']}")
    print(f"  🪙 Criptomoedas: {status['crypto_count']}")
    
    print("\n✅ Exemplo básico concluído!")


if __name__ == '__main__':
    main()
