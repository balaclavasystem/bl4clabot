import os
import tweepy
import discord
from discord.ext import commands
import schedule
import time
import threading
from dotenv import load_dotenv
import asyncio
from openai import OpenAI
import logging
from keep_alive import keep_alive

# Carregar variáveis do .env
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

# Configurações Twitter
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# Configurações Discord
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID") or 0)               # Canal para notificações gerais
DISCORD_GM_CHANNEL_ID = int(os.getenv("DISCORD_GM_CHANNEL_ID") or 0)         # Canal para mensagem fixa GM
DISCORD_NEW_MEMBER_CHANNEL_ID = 1378199753484926976                      # Canal onde o usuário envia NEW MEMBER para revisão
DISCORD_APPROVED_MEMBER_CHANNEL_ID = 1378564229061415023                 # Canal onde será salvo perfil aprovado
DISCORD_ANNOUNCEMENT_CHANNEL_ID = 1333169997228281978                    # Canal de anúncios para o comando /talk

# Configurar autenticação Twitter (API v1.1)
auth = tweepy.OAuth1UserHandler(
   API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)
api_twitter_v1 = tweepy.API(auth)

# Configurar cliente OpenAI (API >= 1.0.0)
client_openai = OpenAI()

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
        logging.warning("⚠️ Arquivo tweets.txt não encontrado.")
    return tweets

tweets_prontos = carregar_tweets_do_arquivo()

# Função para pegar o tweet do dia baseado no dia do mês
def tweet_do_dia():
    if not tweets_prontos:
        logging.warning("⚠️ Nenhum tweet encontrado no arquivo.")
        return None
    import datetime
    dia = datetime.datetime.utcnow().day
    indice = (dia - 1) % len(tweets_prontos)
    logging.info(f"Selecionando tweet do dia: índice {indice}")
    return tweets_prontos[indice]

# Configurar bot Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Enviar mensagem em canal Discord (para notificações)
async def enviar_mensagem_discord(mensagem):
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send(mensagem)
        logging.info(f"Mensagem enviada no Discord: {mensagem}")
    else:
        logging.error("❌ Canal Discord para notificações não encontrado")

# Função para postar tweet do dia e avisar no Discord
def postar_tweet_diario():
    texto = tweet_do_dia()
    if texto:
        try:
            response = api_twitter_v1.update_status(status=texto)
            tweet_url = f"https://twitter.com/user/status/{response.id_str}"
            logging.info(f"✅ Tweet enviado: {tweet_url}")
            asyncio.run_coroutine_threadsafe(
                enviar_mensagem_discord(f"✅ Tweet automático enviado!\n🔗 {tweet_url}"),
                bot.loop
            )
        except Exception as e:
            logging.error(f"❌ Erro ao enviar tweet: {e}")
    else:
        logging.warning("⚠️ Não há tweet para enviar hoje!")

# Enviar mensagem fixa "GM from Valoris" no Discord
async def enviar_gm_valoris_discord():
    mensagem = tweet_do_dia() or "GM from Valoris"
    channel = bot.get_channel(DISCORD_GM_CHANNEL_ID)
    if channel:
        await channel.send(mensagem)
        logging.info(f"Mensagem GM enviada no Discord: {mensagem}")
    else:
        logging.error("❌ Canal Discord para GM não encontrado")

def agendar_gm_discord():
    asyncio.run_coroutine_threadsafe(enviar_gm_valoris_discord(), bot.loop)

# Agendar tarefas
schedule.every().day.at("09:00").do(agendar_gm_discord)      # Mensagem fixa no Discord às 09:00 UTC
schedule.every().day.at("12:00").do(postar_tweet_diario)     # Tweet do arquivo às 12:00 UTC

# Thread para rodar o agendador em background
def agendador():
    while True:
        logging.info(f"Horário atual UTC: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}")
        schedule.run_pending()
        time.sleep(60)

threading.Thread(target=agendador, daemon=True).start()

# Função para gerar perfil do novo membro via OpenAI
async def gerar_perfil_openai(descricao):
    prompt = f"""
Using the Balaclava System tone and style, create a profile for a new member based on this description:

{descricao}

Format the response as:

NAME
AGE
DISTRICT
MEMBER SINCE

Bio:
[Write the biography in English, concise and impactful, keeping the tone poetic, urban and mysterious.]

Always write in English.
"""
    try:
        response = client_openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a creative assistant for the Balaclava System project."},
                {"role": "user", "content": prompt}
            ]
        )
        perfil = response.choices[0].message.content.strip()
        return perfil
    except Exception as e:
        return f"Error generating profile: {e}"

@bot.event
async def on_ready():
    logging.info(f"🤖 Bot Discord conectado como {bot.user}")

# Comando /tweet para enviar tweet na hora com texto customizado
@bot.command()
async def tweet(ctx, *, mensagem):
    try:
        response = api_twitter_v1.update_status(status=mensagem)
        tweet_url = f"https://twitter.com/user/status/{response.id_str}"
        await ctx.send(f"✅ Tweet enviado!\n🔗 {tweet_url}")
    except Exception as e:
        await ctx.send(f"❌ Erro ao enviar tweet: {e}")

# Comando /newmember para gerar perfil do membro e enviar no canal de revisão
@bot.command()
async def newmember(ctx, *, descricao):
    await ctx.message.delete()  # Apaga mensagem original para manter o canal limpo
    perfil_gerado = await gerar_perfil_openai(descricao)
    if perfil_gerado.startswith("Error generating profile"):
        await ctx.send(perfil_gerado)
        return

    canal_revisao = bot.get_channel(DISCORD_NEW_MEMBER_CHANNEL_ID)
    if not canal_revisao:
        await ctx.send("❌ Canal de revisão para novos membros não encontrado.")
        return

    mensagem_envio = (
        f"🆕 **New Member Profile Generated - Review Required**\n\n"
        f"**Description:** {descricao}\n\n"
        f"**Generated Profile:**\n{perfil_gerado}\n\n"
        f"⚠️ Please review and approve or request changes."
    )

    await canal_revisao.send(mensagem_envio)
    await ctx.send("✅ Profile generated and sent for review.")

# Comando /approveprofile para aprovar e salvar no canal de aprovados
@bot.command()
async def approveprofile(ctx, *, perfil):
    # Esse comando deve ser usado no canal de revisão para aprovar o perfil
    canal_aprovados = bot.get_channel(DISCORD_APPROVED_MEMBER_CHANNEL_ID)
    if not canal_aprovados:
        await ctx.send("❌ Canal de aprovados não encontrado.")
        return

    await canal_aprovados.send(f"✅ **Approved Member Profile:**\n\n{perfil}")
    await ctx.send("✅ Profile approved and saved.")

# Comando /talk para enviar mensagem em um canal específico
@bot.command()
@commands.has_permissions(administrator=True)
async def talk(ctx, *, mensagem):
    """Envia uma mensagem do canal de comando para o canal de anúncios."""

    # Verifica se o comando foi usado no canal correto
    if ctx.channel.id != DISCORD_NEW_MEMBER_CHANNEL_ID:
        await ctx.message.delete()
        await ctx.send(f"Este comando só pode ser usado em <#{DISCORD_NEW_MEMBER_CHANNEL_ID}>.", delete_after=10)
        return

    # Deleta a mensagem de comando para manter o canal limpo
    await ctx.message.delete()

    canal_anuncios = bot.get_channel(DISCORD_ANNOUNCEMENT_CHANNEL_ID)
    if canal_anuncios:
        try:
            await canal_anuncios.send(mensagem)
            # Envia uma confirmação temporária
            await ctx.send(f"✅ Mensagem enviada para {canal_anuncios.mention}.", delete_after=10)
            logging.info(f"Mensagem enviada via /talk por {ctx.author.name}: '{mensagem}'")
        except Exception as e:
            await ctx.send(f"❌ Ocorreu um erro ao enviar a mensagem: {e}", delete_after=10)
            logging.error(f"Erro no comando /talk: {e}")
    else:
        await ctx.send("❌ Canal de anúncios não encontrado. Verifique o ID.", delete_after=10)
        logging.warning(f"Canal de anúncios ({DISCORD_ANNOUNCEMENT_CHANNEL_ID}) não encontrado ao usar /talk.")

keep_alive()
bot.run(DISCORD_TOKEN)
