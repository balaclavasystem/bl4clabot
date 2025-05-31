import os
import tweepy
import discord
from discord.ext import commands
import schedule
import time
import threading
from dotenv import load_dotenv
import asyncio

from keep_alive import keep_alive
keep_alive()

# Carregar variáveis do .env
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Canal para notificações de tweets enviados
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

# Canal para enviar a mensagem "GM from Valoris"
DISCORD_GM_CHANNEL_ID = int(os.getenv("DISCORD_GM_CHANNEL_ID"))

# Configurar autenticação Twitter (Client V2)
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Função para carregar tweets do arquivo tweets.txt
def carregar_tweets_do_arquivo():
    tweets = []
    try:
        with open("tweets.txt", "r", encoding="utf-8") as f:
            conteudo = f.read()
            blocos = conteudo.split("\n\n")  # separa por linhas vazias
            for bloco in blocos:
                bloco = bloco.strip()
                if bloco:
                    tweets.append(bloco)
    except FileNotFoundError:
        print("⚠️ Arquivo tweets.txt não encontrado.")
    return tweets

tweets_prontos = carregar_tweets_do_arquivo()

# Configurar bot Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Enviar mensagem em canal Discord (para notificações)
async def enviar_mensagem_discord(mensagem):
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send(mensagem)
    else:
        print("❌ Canal Discord para notificações não encontrado")

# Enviar tweet do arquivo e notificar Discord
def postar_tweet_diario():
    if tweets_prontos:
        mensagem = tweets_prontos.pop(0)
        try:
            response = client.create_tweet(text=mensagem)
            tweet_url = f"https://twitter.com/user/status/{response.data['id']}"
            print(f"✅ Tweet enviado: {tweet_url}")
            asyncio.run_coroutine_threadsafe(
                enviar_mensagem_discord(f"✅ Tweet automático enviado!\n🔗 {tweet_url}"),
                bot.loop
            )
        except Exception as e:
            print(f"❌ Erro ao enviar tweet: {e}")
    else:
        print("⚠️ Todos os tweets foram enviados!")

# Enviar mensagem fixa "GM from Valoris" no Discord
async def enviar_gm_valoris_discord():
    mensagem = "GM from Valoris"
    channel = bot.get_channel(DISCORD_GM_CHANNEL_ID)
    if channel:
        await channel.send(mensagem)
        print("✅ Mensagem 'GM from Valoris' enviada no Discord")
    else:
        print("❌ Canal Discord para GM não encontrado")

def agendar_gm_discord():
    asyncio.run_coroutine_threadsafe(enviar_gm_valoris_discord(), bot.loop)

# Agendar tarefas
schedule.every().day.at("12:00").do(agendar_gm_discord)      # Mensagem fixa no Discord
schedule.every().day.at("12:00").do(postar_tweet_diario)     # Tweet do arquivo

# Thread para rodar o agendador em background
def agendador():
    while True:
        print("Horário atual UTC:", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
        schedule.run_pending()
        time.sleep(60)

threading.Thread(target=agendador, daemon=True).start()

@bot.event
async def on_ready():
    print(f"🤖 Bot Discord conectado como {bot.user}")

@bot.command()
async def tweet(ctx, *, mensagem):
    try:
        response = client.create_tweet(text=mensagem)
        tweet_url = f"https://twitter.com/user/status/{response.data['id']}"
        await ctx.send(f"✅ Tweet enviado!\n🔗 {tweet_url}")
    except Exception as e:
        await ctx.send(f"❌ Erro ao enviar tweet: {e}")

bot.run(DISCORD_TOKEN)
