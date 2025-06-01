import os
import tweepy
import discord
from discord.ext import commands
import schedule
import time
import threading
from dotenv import load_dotenv
import asyncio
import openai

from keep_alive import keep_alive
keep_alive()

# Carregar variáveis do .env
load_dotenv()

API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Canais
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))           # Para tweet notifications
DISCORD_GM_CHANNEL_ID = int(os.getenv("DISCORD_GM_CHANNEL_ID"))     # Para "GM from Valoris"
REVIEW_CHANNEL_ID = 1378199753484926976                             # Para revisão de perfis
FINAL_CHANNEL_ID = 1378564229061415023                              # Canal final aprovado

# Configurar Twitter
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Configurar OpenAI
openai.api_key = OPENAI_API_KEY

# Carregar tweets do arquivo
def carregar_tweets_do_arquivo():
    tweets = []
    try:
        with open("tweets.txt", "r", encoding="utf-8") as f:
            conteudo = f.read()
            blocos = conteudo.split("\n\n")
            for bloco in blocos:
                bloco = bloco.strip()
                if bloco:
                    tweets.append(bloco)
    except FileNotFoundError:
        print("⚠️ Arquivo tweets.txt não encontrado.")
    return tweets

tweets_prontos = carregar_tweets_do_arquivo()

def tweet_do_dia():
    if not tweets_prontos:
        print("⚠️ Nenhum tweet encontrado.")
        return None
    import datetime
    dia = datetime.datetime.utcnow().day
    indice = (dia - 1) % len(tweets_prontos)
    return tweets_prontos[indice]

# Discord Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

async def enviar_mensagem_discord(mensagem):
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send(mensagem)
    else:
        print("❌ Canal Discord não encontrado.")

# GM automático
async def enviar_gm_valoris_discord():
    mensagem = "GM from Valoris"
    channel = bot.get_channel(DISCORD_GM_CHANNEL_ID)
    if channel:
        await channel.send(mensagem)
        print("✅ GM enviado")
    else:
        print("❌ Canal GM não encontrado.")

def agendar_gm_discord():
    asyncio.run_coroutine_threadsafe(enviar_gm_valoris_discord(), bot.loop)

# Tweet diário
def postar_tweet_diario():
    texto = tweet_do_dia()
    if texto:
        try:
            response = client.create_tweet(text=texto)
            tweet_url = f"https://twitter.com/user/status/{response.data['id']}"
            print(f"✅ Tweet enviado: {tweet_url}")
            asyncio.run_coroutine_threadsafe(
                enviar_mensagem_discord(f"✅ Tweet automático enviado!\n🔗 {tweet_url}"),
                bot.loop
            )
        except Exception as e:
            print(f"❌ Erro ao enviar tweet: {e}")
    else:
        print("⚠️ Tweet do dia vazio.")

# Agendador de tarefas
schedule.every().day.at("09:00").do(agendar_gm_discord)
schedule.every().day.at("12:00").do(postar_tweet_diario)

def agendador():
    while True:
        print("🕐 Horário UTC:", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
        schedule.run_pending()
        time.sleep(60)

threading.Thread(target=agendador, daemon=True).start()

@bot.event
async def on_ready():
    print(f"🤖 Conectado como {bot.user}")

# Comando /tweet
@bot.command()
async def tweet(ctx, *, mensagem):
    try:
        response = client.create_tweet(text=mensagem)
        tweet_url = f"https://twitter.com/user/status/{response.data['id']}"
        await ctx.send(f"✅ Tweet enviado!\n🔗 {tweet_url}")
    except Exception as e:
        await ctx.send(f"❌ Erro ao enviar tweet: {e}")

# Comando /newmember
BALACLAVA_SYSTEM_PROMPT = """
You are the creative consultant and storyteller for the Balaclava System, a Web3 art universe. Given a short description of a character, generate a new citizen of Valoris in the following format, in English:

NAME: [Invent a realistic, cool name]
AGE: [Choose an age that fits the vibe]
BIO: [Write a short paragraph in the Balaclava System tone: poetic, mysterious, urban, inspired by the streets, slightly philosophical. Around 3-6 lines.]

Do not include any hashtags, emojis or markdown. Only return the formatted text.
"""

@bot.command()
async def newmember(ctx, *, description):
    await ctx.send("🧠 Generating new member profile...")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": BALACLAVA_SYSTEM_PROMPT},
                {"role": "user", "content": description}
            ],
            temperature=0.8,
            max_tokens=250
        )

        generated_profile = response.choices[0].message.content.strip()

        review_channel = bot.get_channel(REVIEW_CHANNEL_ID)
        if review_channel:
            await review_channel.send(f"🆕 NEW MEMBER PROFILE (review before approval):\n\n{generated_profile}")
            await ctx.send("✅ Profile sent to review channel.")
        else:
            await ctx.send("❌ Review channel not found.")
    except Exception as e:
        await ctx.send(f"❌ Error generating profile: {e}")

# Iniciar bot
bot.run(DISCORD_TOKEN)
