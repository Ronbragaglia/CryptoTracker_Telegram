# 🚀 Crypto Tracker Telegram 📊

Monitoramento Automático de Criptomoedas com Alertas no Telegram

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

O **Crypto Tracker Telegram** é uma ferramenta poderosa de automação para monitoramento de criptomoedas em tempo real. Desenvolvido com Python, Selenium e Telegram Bot API, ele coleta automaticamente dados de criptomoedas, armazena em banco de dados, gera gráficos e envia alertas automáticos.

## ✨ Funcionalidades

- 🤖 **Coleta automática de dados** de criptomoedas do CoinGecko
- 📊 **Armazenamento em banco de dados** SQLite com histórico completo
- 📈 **Geração automática de gráficos** de Market Cap e variações
- 🔔 **Alertas automáticos** para variações bruscas via Telegram
- ⏰ **Agendamento automático** - execute a cada X horas sem intervenção manual
- 🎯 **Configuração avançada** - proxy, timeouts, rate limiting e mais
- 📱 **Notificações flexíveis** - via Telegram com suporte a Markdown
- 💾 **Backup automático** do banco de dados
- 🐳 **Suporte a Docker** - execute em containers facilmente
- 🧪 **Suporte a múltiplas criptomoedas** - Bitcoin, Ethereum, etc.

## 🛠️ Tecnologias Utilizadas

- **Python 3.9+** - Linguagem principal
- **Selenium** - Automação de navegação web
- **Undetected ChromeDriver** - WebDriver que evita detecção
- **Pandas** - Manipulação e análise de dados
- **Matplotlib** - Geração de gráficos
- **SQLite** - Banco de dados local
- **Telegram Bot API** - Envio de notificações
- **Schedule** - Agendamento de tarefas

## 📋 Pré-requisitos

- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)
- Chrome ou Chromium (para execução local)
- Telegram Bot configurado (veja [Configurar Telegram Bot](#configurar-telegram-bot))

## 🚀 Instalação Rápida

### Via pip

```bash
# Clone o repositório
git clone https://github.com/Ronbragaglia/CryptoTracker_Telegram.git
cd CryptoTracker_Telegram

# Instale as dependências
pip install -r requirements.txt

# Configure o Telegram Bot (veja abaixo)
cp .env.example .env
# Edite o arquivo .env com suas credenciais

# Execute o tracker
python -m crypto_tracker --scheduled
```

### Via Docker

```bash
# Clone o repositório
git clone https://github.com/Ronbragaglia/CryptoTracker_Telegram.git
cd CryptoTracker_Telegram

# Construa a imagem Docker
docker build -t crypto-tracker .

# Execute o container
docker run --rm -v $(pwd)/data:/app/data -v $(pwd)/logs:/app/logs crypto-tracker
```

### Via Docker Compose

```bash
# Clone o repositório
git clone https://github.com/Ronbragaglia/CryptoTracker_Telegram.git
cd CryptoTracker_Telegram

# Execute com Docker Compose
docker-compose up crypto-tracker
```

## ⚙️ Configuração

### Configurar Telegram Bot

Para usar este projeto, você precisa criar seu próprio bot do Telegram:

1. **Abra o Telegram** e procure pelo [@BotFather](https://t.me/botfather)
2. **Crie um novo bot** com o comando `/newbot`
3. **Copie o token** fornecido pelo BotFather
4. **Obtenha seu Chat ID**:
   - Envie uma mensagem para o seu bot
   - Acesse: `https://api.telegram.org/bot<SEU_TOKEN>/getUpdates`
   - Encontre seu `chat_id` na resposta
5. **Configure o arquivo `.env`**:
   ```env
   TELEGRAM_BOT_TOKEN=seu_bot_token_aqui
   TELEGRAM_CHAT_ID=seu_chat_id_aqui
   ```

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto baseado no [`.env.example`](.env.example):

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=seu_bot_token_aqui
TELEGRAM_CHAT_ID=seu_chat_id_aqui

# WebDriver Configuration
WEBDRIVER_BROWSER=chrome
WEBDRIVER_HEADLESS=true

# Scraping Configuration
MAX_CRYPTOS=10
COINGECKO_URL=https://www.coingecko.com/pt

# Alert Configuration
ALERT_ENABLED=true
ALERT_THRESHOLD_PERCENT=5.0

# Chart Configuration
CHART_ENABLED=true
CHART_GENERATION_INTERVAL_HOURS=6

# Schedule Configuration
DATA_COLLECTION_INTERVAL_HOURS=2
ALERT_CHECK_INTERVAL_HOURS=1
```

## 📖 Uso

### Uso Básico

```python
from crypto_tracker import CryptoTracker

# Cria instância do tracker
tracker = CryptoTracker()

# Executa uma vez
tracker.run_once()
```

### Uso Avançado

```python
from crypto_tracker import CryptoTracker, DatabaseManager, ChartGenerator
import pandas as pd

# Cria instância do tracker
tracker = CryptoTracker()
db = DatabaseManager()
chart_generator = ChartGenerator()

# Coleta dados
crypto_data = tracker.collect_crypto_data()

# Analisa dados
df = db.get_crypto_history(limit=100)

# Gera gráficos
chart_path = chart_generator.generate_market_cap_chart(df)

# Verifica alertas
alerts = tracker.check_alerts()
```

### Linha de Comando

```bash
# Executa uma vez
python -m crypto_tracker --once

# Executa com agendamento automático
python -m crypto_tracker --scheduled

# Coleta dados de 20 criptomoedas
python -m crypto_tracker --once --max-cryptos 20

# Desabilita alertas
python -m crypto_tracker --once --no-alerts

# Desabilita gráficos
python -m crypto_tracker --once --no-charts

# Mostra status
python -m crypto_tracker --status

# Modo verbose
python -m crypto_tracker --scheduled --verbose

# Ajuda
python -m crypto_tracker --help
```

## 📁 Estrutura do Projeto

```
crypto-tracker-telegram/
├── src/
│   └── crypto_tracker/
│       ├── __init__.py          # Pacote principal
│       ├── __main__.py          # Ponto de entrada
│       ├── cli.py               # Interface de linha de comando
│       ├── config.py            # Configurações
│       ├── logger.py            # Sistema de logging
│       ├── tracker.py           # Tracker principal
│       ├── telegram.py          # Notificações Telegram
│       ├── database.py          # Gerenciamento do banco
│       └── chart.py            # Geração de gráficos
├── tests/                       # Testes
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_tracker.py
│   └── test_config.py
├── examples/                    # Exemplos de uso
│   ├── __init__.py
│   ├── basic_usage.py
│   └── advanced_usage.py
├── data/                        # Diretório de dados
├── logs/                        # Diretório de logs
├── docs/                        # Documentação
├── .github/workflows/           # CI/CD
├── .env.example                 # Exemplo de configuração
├── .gitignore
├── .pre-commit-config.yaml
├── Dockerfile
├── docker-compose.yml
├── LICENSE
├── Makefile
├── pyproject.toml
├── README.md
└── requirements.txt
```

## 🧪 Criptomoedas Suportadas

Atualmente, o tracker suporta as principais criptomoedas listadas no CoinGecko:

- Bitcoin (BTC)
- Ethereum (ETH)
- Tether (USDT)
- Binance Coin (BNB)
- Solana (SOL)
- XRP (XRP)
- USDC
- Cardano (ADA)
- Avalanche (AVAX)
- Dogecoin (DOGE)

*E muitas outras conforme disponíveis no CoinGecko*

## 📊 Funcionalidades Avançadas

### Análise de Dados

```python
from crypto_tracker import DatabaseManager
import pandas as pd

db = DatabaseManager()
df = db.get_crypto_history(limit=100)

# Top 5 criptomoedas por Market Cap
df['market_cap_float'] = df['market_cap'].str.replace('US$', '').str.replace(',', '').astype(float)
top_cryptos = df.groupby('name')['market_cap_float'].last().sort_values(ascending=False).head(5)
print(top_cryptos)
```

### Geração de Gráficos Personalizados

```python
from crypto_tracker import ChartGenerator

chart_generator = ChartGenerator()

# Gráfico de histórico
chart_generator.generate_market_cap_chart(df)

# Gráfico de comparação
chart_generator.generate_crypto_comparison_chart(df)

# Gráfico de variação
chart_generator.generate_variation_chart(df)
```

### Backup Automático

```python
from crypto_tracker import DatabaseManager

db = DatabaseManager()
db.backup_database()  # Backup automático
db.cleanup_old_data(days=30)  # Limpeza de dados antigos
```

## 🧪 Testes

```bash
# Execute todos os testes
pytest

# Execute com cobertura
pytest --cov=src/crypto_tracker --cov-report=html --cov-report=term-missing

# Execute testes específicos
pytest tests/test_tracker.py

# Execute em modo verbose
pytest -v
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, leia o [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Rone Bragaglia**

- GitHub: [@Ronbragaglia](https://github.com/Ronbragaglia)
- Email: rone.bragaglia@uni9.edu.br
- LinkedIn: [linkedin.com/in/rone-bragaglia-a6aa60157](https://linkedin.com/in/rone-bragaglia-a6aa60157)

## 🙏 Agradecimentos

- A todos os contribuidores que ajudaram a melhorar este projeto
- Às comunidades Python e Selenium pelos excelentes recursos
- Ao CoinGecko por disponibilizar os dados de criptomoedas
- Ao Telegram pela excelente API de bots

## 📞 Suporte

Se você encontrar algum problema ou tiver alguma dúvida:

1. Verifique a [documentação](docs/)
2. Procure [issues existentes](https://github.com/Ronbragaglia/CryptoTracker_Telegram/issues)
3. Crie uma nova [issue](https://github.com/Ronbragaglia/CryptoTracker_Telegram/issues/new)

## 🗺️ Roadmap

- [ ] Suporte a mais exchanges
- [ ] Integração com APIs de trading
- [ ] Sistema de recomendação de criptomoedas
- [ ] Dashboard web
- [ ] Alertas personalizados
- [ ] Integração com Discord
- [ ] Exportação em múltiplos formatos
- [ ] Análise de tendências com IA

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no GitHub!
