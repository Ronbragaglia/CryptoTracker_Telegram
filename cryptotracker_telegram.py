# -*- coding: utf-8 -*-
"""CryptoTracker_Telegram

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DC9sFQ02kE7Uc_N9Xx3mXQbPIwPUH-lP
"""

!pip install selenium pandas openpyxl undetected-chromedriver

import time
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

options = uc.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = uc.Chrome(options=options)

url = "https://www.coingecko.com/pt"
driver.get(url)

time.sleep(3)


moedas = driver.find_elements(By.XPATH, '//tbody/tr')

dados = []
for moeda in moedas[:20]:
    try:
        nome = moeda.find_element(By.XPATH, './/td[3]//a').text
        preco = moeda.find_element(By.XPATH, './/td[4]//span').text
        variacao_24h = moeda.find_element(By.XPATH, './/td[5]').text
        variacao_7d = moeda.find_element(By.XPATH, './/td[6]').text
        volume_mercado = moeda.find_element(By.XPATH, './/td[8]').text
        market_cap = moeda.find_element(By.XPATH, './/td[10]').text

        try:
            fornecimento_total = moeda.find_element(By.XPATH, './/td[9]').text
        except:
            fornecimento_total = "N/A"

        dados.append([nome, preco, variacao_24h, variacao_7d, volume_mercado, market_cap, fornecimento_total])
    except:
        continue


driver.quit()


df = pd.DataFrame(dados, columns=['Nome', 'Preço', 'Variação 24h', 'Variação 7d', 'Volume de Mercado', 'Market Cap', 'Fornecimento Total'])


df.to_excel("dados_criptomoedas_completo.xlsx", index=False)


df.head()

import time
import random
import pandas as pd
import matplotlib.pyplot as plt
import undetected_chromedriver as uc
import requests
from io import BytesIO
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = uc.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = uc.Chrome(options=options)


url = "https://www.coingecko.com/pt"
driver.get(url)

try:
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table tbody tr')))
    print("✅ Página carregada com sucesso!")
except Exception as e:
    print(f"❌ Erro ao carregar a página: {e}")
    driver.quit()
    exit()

moedas = driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')
print(f"🔍 Total de criptomoedas encontradas: {len(moedas)}")

dados = []
for i, moeda in enumerate(moedas[:10]):
    try:
        print(f"\n🔍 Coletando dados da moeda {i+1}...")

        nome = moeda.find_element(By.CSS_SELECTOR, 'td:nth-child(3) a').text
        market_cap = moeda.find_element(By.CSS_SELECTOR, 'td:nth-child(10)').text

        print(f"🔹 {nome} - Market Cap: {market_cap}")


        market_cap_value = int(''.join(filter(str.isdigit, market_cap)))

        dados.append([nome, market_cap_value])

        time.sleep(random.uniform(3, 6))

    except Exception as e:
        print(f"❌ Erro ao coletar dados da moeda {i+1}: {e}")
        continue


df = pd.DataFrame(dados, columns=['Nome', 'Market Cap'])


plt.figure(figsize=(12, 6))
plt.bar(df['Nome'], df['Market Cap'], color='blue')
plt.xlabel("Criptomoedas")
plt.ylabel("Market Cap (US$)")
plt.title("Comparação de Market Cap das Principais Criptomoedas")
plt.xticks(rotation=45)
plt.savefig("market_cap_bar.png")
plt.show()

plt.figure(figsize=(8, 8))
plt.pie(df['Market Cap'][:5], labels=df['Nome'][:5], autopct='%1.1f%%', startangle=140)
plt.title("Participação das 5 maiores Criptomoedas no Market Cap")
plt.savefig("market_cap_pizza.png")

df.to_excel("dados_criptomoedas.xlsx", index=False)


driver.quit()


TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""

def enviar_telegram(mensagem, imagem=None):
    url_mensagem = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    url_foto = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"


    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensagem}
    requests.post(url_mensagem, data=payload)


    if imagem:
        with open(imagem, "rb") as foto:
            files = {"photo": foto}
            data = {"chat_id": TELEGRAM_CHAT_ID}
            requests.post(url_foto, data=data, files=files)

mensagem_cripto = f"📊 Dados Atualizados das Principais Criptomoedas:\n\n{df.to_string(index=False)}"
enviar_telegram(mensagem_cripto)
enviar_telegram("📊 Gráfico de Market Cap das Criptomoedas", "market_cap_bar.png")
enviar_telegram("🥧 Participação das 5 maiores Criptomoedas", "market_cap_pizza.png")

print("🚀 Dados enviados para o Telegram com sucesso!")

import time
import schedule
import sqlite3
import pandas as pd
import requests
from datetime import datetime
from telegram import Bot


TELEGRAM_TOKEN = ""
TELEGRAM_CHAT_ID = ""
bot = Bot(token=TELEGRAM_TOKEN)

conn = sqlite3.connect("crypto_data.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS cryptos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        name TEXT,
        market_cap TEXT
    )
""")
conn.commit()

def coletar_dados():
    print("✅ Coletando dados...")
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": "false"
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        for coin in data:
            name = coin["name"]
            market_cap = f'US$ {coin["market_cap"]:,}'
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


            cursor.execute("INSERT INTO cryptos (timestamp, name, market_cap) VALUES (?, ?, ?)",
                           (timestamp, name, market_cap))
            conn.commit()
            print(f'🔹 {name} - Market Cap: {market_cap}')


            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f'🚀 {name} - Market Cap: {market_cap}')
    else:
        print("❌ Erro ao buscar dados")

schedule.every(1).hours.do(coletar_dados)

print("🔄 Iniciando o monitor de criptomoedas...")
while True:
    schedule.run_pending()
    time.sleep(60)

import time
import schedule
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import undetected_chromedriver as uc
import asyncio
from selenium.webdriver.common.by import By
from telegram import Bot

options = uc.ChromeOptions()
options.headless = True
driver = uc.Chrome(options=options)

TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""
bot = Bot(token=TELEGRAM_BOT_TOKEN)

conn = sqlite3.connect("crypto_data.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS criptomoedas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        market_cap TEXT,
        data TEXT DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

def coletar_dados():
    print("🔄 Buscando dados...")
    url = "https://www.coingecko.com/pt"
    driver.get(url)
    time.sleep(5)

    criptos = driver.find_elements(By.XPATH, "//tbody/tr")[:10]

    lista_dados = []
    message = "📊 **Atualização das Criptomoedas:**\n"

    for i, cripto in enumerate(criptos, start=1):
        try:
            nome = cripto.find_element(By.XPATH, ".//td[3]//a").text
            market_cap = cripto.find_element(By.XPATH, ".//td[7]").text
            lista_dados.append((nome, market_cap))
            message += f"\n🔹 {nome} - Market Cap: {market_cap}"

            cursor.execute("INSERT INTO criptomoedas (nome, market_cap) VALUES (?, ?)", (nome, market_cap))
            conn.commit()
        except Exception as e:
            print(f"⚠️ Erro ao coletar dados da moeda {i}: {e}")

    print("✅ Dados coletados com sucesso!")

    asyncio.run(enviar_mensagem_telegram(message))

    return lista_dados

async def enviar_mensagem_telegram(message):
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

def gerar_grafico():
    df = pd.read_sql_query("SELECT nome, market_cap, data FROM criptomoedas", conn)

    if df.empty:
        print("⚠️ Sem dados suficientes para gerar gráficos.")
        return

    df["market_cap"] = df["market_cap"].str.replace("US$", "").str.replace(",", "").astype(float)

    plt.figure(figsize=(12, 6))
    for nome in df["nome"].unique():
        dados = df[df["nome"] == nome]
        plt.plot(dados["data"], dados["market_cap"], marker="o", label=nome)

    plt.title("Histórico de Market Cap das Criptomoedas")
    plt.xlabel("Data")
    plt.ylabel("Market Cap (USD)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()


def verificar_alertas():
    df = pd.read_sql_query("SELECT nome, market_cap FROM criptomoedas ORDER BY data DESC LIMIT 20", conn)

    if df.empty:
        return

    df["market_cap"] = df["market_cap"].str.replace("US$", "").str.replace(",", "").astype(float)
    alertas = []

    for _, row in df.iterrows():
        nome = row["nome"]
        market_cap_atual = row["market_cap"]

        cursor.execute("SELECT market_cap FROM criptomoedas WHERE nome = ? ORDER BY data DESC LIMIT 2", (nome,))
        historico = cursor.fetchall()

        if len(historico) < 2:
            continue

        market_cap_anterior = float(historico[1][0].replace("US$", "").replace(",", ""))

        variacao = ((market_cap_atual - market_cap_anterior) / market_cap_anterior) * 100

        if abs(variacao) > 5:
            alertas.append(f"⚠️ {nome} teve uma variação de {variacao:.2f}%!")

    if alertas:
        asyncio.run(enviar_mensagem_telegram("\n".join(alertas)))

schedule.every(2).hours.do(coletar_dados)
schedule.every(6).hours.do(gerar_grafico)
schedule.every(1).hour.do(verificar_alertas)


print("🔄 Iniciando o monitor de criptomoedas...")
while True:
    schedule.run_pending()
    time.sleep(60)
