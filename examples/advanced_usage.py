#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo avançado de uso do Crypto Tracker Telegram.

Este exemplo demonstra recursos avançados como:
- Configuração personalizada
- Análise de dados
- Geração de gráficos personalizados
- Verificação de alertas
"""

import pandas as pd
from pathlib import Path

from crypto_tracker import CryptoTracker, DatabaseManager, ChartGenerator, TelegramNotifier
from crypto_tracker.config import config


def main():
    """Função principal do exemplo avançado."""
    print("=" * 80)
    print("🚀 Exemplo Avançado do Crypto Tracker Telegram")
    print("=" * 80)
    
    # Exemplo 1: Configuração personalizada
    print("\n📌 Exemplo 1: Configuração Personalizada")
    print(f"  📊 Máximo de criptomoedas: {config.scraping.max_cryptos}")
    print(f"  ⏰ Intervalo de coleta: {config.schedule.data_collection_interval_hours} horas")
    print(f"  🔔 Alertas habilitados: {config.alert.enabled}")
    print(f"  📊 Gráficos habilitados: {config.chart.enabled}")
    
    # Exemplo 2: Coleta de dados
    print("\n📌 Exemplo 2: Coleta de Dados")
    tracker = CryptoTracker()
    crypto_data = tracker.collect_crypto_data()
    print(f"  ✅ {len(crypto_data)} criptomoedas coletadas")
    
    # Exemplo 3: Análise de dados
    print("\n📌 Exemplo 3: Análise de Dados")
    db = DatabaseManager()
    df = db.get_crypto_history(limit=50)
    
    if not df.empty:
        # Criptomoedas com maior market cap
        df['market_cap_float'] = df['market_cap'].str.replace('US$', '').str.replace(',', '').astype(float)
        top_cryptos = df.groupby('name')['market_cap_float'].last().sort_values(ascending=False).head(5)
        print("  🏆 Top 5 Criptomoedas por Market Cap:")
        for name, market_cap in top_cryptos.items():
            print(f"     - {name}: ${market_cap:,.0f}")
        
        # Variação das criptomoedas
        print("\n  📈 Variação das Criptomoedas (24h):")
        for name in db.get_all_crypto_names()[:5]:
            variation = db.get_crypto_variation(name, hours=24)
            if variation is not None:
                emoji = "📈" if variation >= 0 else "📉"
                print(f"     {emoji} {name}: {variation:.2f}%")
    
    # Exemplo 4: Verificação de alertas
    print("\n📌 Exemplo 4: Verificação de Alertas")
    alerts = tracker.check_alerts()
    if alerts:
        print(f"  ⚠️ {len(alerts)} alertas enviados")
    else:
        print("  ✅ Nenhum alerta para enviar")
    
    # Exemplo 5: Geração de gráficos
    print("\n📌 Exemplo 5: Geração de Gráficos")
    chart_generator = ChartGenerator()
    
    if not df.empty:
        # Gráfico de histórico
        chart_path = chart_generator.generate_market_cap_chart(df)
        if chart_path:
            print(f"  ✅ Gráfico de histórico gerado: {chart_path}")
        
        # Gráfico de comparação
        comparison_path = chart_generator.generate_crypto_comparison_chart(df)
        if comparison_path:
            print(f"  ✅ Gráfico de comparação gerado: {comparison_path}")
        
        # Gráfico de variação
        variation_path = chart_generator.generate_variation_chart(df)
        if variation_path:
            print(f"  ✅ Gráfico de variação gerado: {variation_path}")
    
    # Exemplo 6: Envio de notificações
    print("\n📌 Exemplo 6: Envio de Notificações")
    telegram = TelegramNotifier()
    
    # Testa conexão
    if telegram.test_connection():
        print("  ✅ Conexão com Telegram estabelecida")
    
    # Envia mensagem de teste
    if config.notification.enabled:
        test_message = "🧪 **Teste de Notificação**\n\nO Crypto Tracker está funcionando corretamente!"
        if telegram.send_message(test_message):
            print("  ✅ Mensagem de teste enviada")
    
    # Exemplo 7: Backup do banco de dados
    print("\n📌 Exemplo 7: Backup do Banco de Dados")
    if db.backup_database():
        print("  ✅ Backup do banco de dados criado")
    
    # Exemplo 8: Limpeza de dados antigos
    print("\n📌 Exemplo 8: Limpeza de Dados Antigos")
    deleted = db.cleanup_old_data(days=30)
    if deleted > 0:
        print(f"  ✅ {deleted} registros antigos removidos")
    else:
        print("  ℹ️ Nenhum registro antigo para remover")
    
    # Exemplo 9: Status do rastreador
    print("\n📌 Exemplo 9: Status do Rastreador")
    status = tracker.get_status()
    print(f"  📁 Banco de dados: {status['database_path']}")
    print(f"  📝 Registros: {status['record_count']}")
    print(f"  💾 Tamanho: {status['database_size']} bytes")
    print(f"  🪙 Criptomoedas: {status['crypto_count']}")
    print(f"  📱 Telegram configurado: {status['telegram_configured']}")
    print(f"  🔔 Alertas habilitados: {status['alert_enabled']}")
    print(f"  📊 Gráficos habilitados: {status['chart_enabled']}")
    
    print("\n" + "=" * 80)
    print("✅ Exemplo avançado concluído!")
    print("=" * 80)


if __name__ == '__main__':
    main()
