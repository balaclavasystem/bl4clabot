#!/usr/bin/env python3
"""
Bot Discord BL4CL4 - Versão Render
Otimizada para funcionar no Render.com
"""

import os
import discord
from discord.ext import commands
import schedule
import time
import threading
from dotenv import load_dotenv
import asyncio
import logging
import random
import requests
from flask import Flask

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

# Configurações Discord
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_GM_CHANNEL_ID = int(os.getenv("DISCORD_GM_CHANNEL_ID") or 0)
DISCORD_NEW_MEMBER_CHANNEL_ID = 1378199753484926976
DISCORD_ANNOUNCEMENT_CHANNEL_ID = 1333169997228281978

# Lista de mensagens GM
GM_MESSAGES = [
    "GM from Valoris! 🌅",
    "Good Morning, Valoris community! ☀️",
    "GM! Another day, another opportunity! 🚀",
    "Good Morning! Stay strong, stay Valoris! 💪",
    "GM! Building the future together! 🔮",
    "Good Morning! Keep pushing forward! ⚡",
    "GM! Innovation never sleeps! 🌟",
    "Good Morning! Let's make today count! 🎯",
    "GM! The future is now! 🔥",
    "Good Morning! Together we grow! 🌱",
    "GM! Valoris strong! 💎",
    "Good Morning! Dreams become reality! ✨",
    "GM! Community first! 🤝",
    "Good Morning! Building bridges! 🌉",
    "GM! The revolution continues! 🚀"
]

# Configurar bot Discord com intents completos
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Flask app para keep-alive no Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot BL4CL4 está online! 🤖"

@app.route('/health')
def health():
    return {"status": "online", "bot": "BL4CL4"}

def run_flask():
    """Executa o Flask em uma thread separada"""
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def gm_do_dia():
    """Retorna uma mensagem GM aleatória da lista"""
    return random.choice(GM_MESSAGES)

async def enviar_gm_discord():
    """Envia mensagem GM no Discord"""
    try:
        mensagem = gm_do_dia()
        channel = bot.get_channel(DISCORD_GM_CHANNEL_ID)
        if channel:
            await channel.send(mensagem)
            logging.info(f"✅ Mensagem GM enviada: {mensagem}")
        else:
            logging.error(f"❌ Canal GM não encontrado: {DISCORD_GM_CHANNEL_ID}")
    except Exception as e:
        logging.error(f"❌ Erro ao enviar GM: {e}")

def agendar_gm():
    """Agenda o envio da mensagem GM"""
    try:
        asyncio.run_coroutine_threadsafe(enviar_gm_discord(), bot.loop)
    except Exception as e:
        logging.error(f"❌ Erro ao agendar GM: {e}")

# Agendar GM diário às 9:00
schedule.every().day.at("09:00").do(agendar_gm)

def agendador():
    """Thread para rodar o agendador em background"""
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)
        except Exception as e:
            logging.error(f"❌ Erro no agendador: {e}")
            time.sleep(60)

def keep_alive():
    """Função para manter o bot vivo no Render"""
    while True:
        try:
            # Ping para o próprio servidor
            response = requests.get("http://localhost:8080/health", timeout=10)
            if response.status_code == 200:
                logging.info("✅ Keep-alive ping realizado")
            else:
                logging.warning(f"⚠️ Keep-alive retornou status {response.status_code}")
        except Exception as e:
            logging.error(f"❌ Erro no keep-alive: {e}")
        
        time.sleep(300)  # Ping a cada 5 minutos

@bot.event
async def on_ready():
    """Evento quando o bot conecta"""
    logging.info(f"🤖 Bot conectado como {bot.user}")
    logging.info(f"🆔 ID do bot: {bot.user.id}")
    logging.info(f"🏠 Servidores: {len(bot.guilds)}")
    
    # Verificar canais
    new_member_channel = bot.get_channel(DISCORD_NEW_MEMBER_CHANNEL_ID)
    announcement_channel = bot.get_channel(DISCORD_ANNOUNCEMENT_CHANNEL_ID)
    gm_channel = bot.get_channel(DISCORD_GM_CHANNEL_ID)
    
    if new_member_channel:
        logging.info(f"✅ Canal de comando: {new_member_channel.name}")
    else:
        logging.warning(f"❌ Canal de comando não encontrado: {DISCORD_NEW_MEMBER_CHANNEL_ID}")
    
    if announcement_channel:
        logging.info(f"✅ Canal de anúncios: {announcement_channel.name}")
    else:
        logging.warning(f"❌ Canal de anúncios não encontrado: {DISCORD_ANNOUNCEMENT_CHANNEL_ID}")
    
    if gm_channel:
        logging.info(f"✅ Canal GM: {gm_channel.name}")
    else:
        logging.warning(f"❌ Canal GM não encontrado: {DISCORD_GM_CHANNEL_ID}")

@bot.event
async def on_disconnect():
    """Evento quando o bot desconecta"""
    logging.warning("⚠️ Bot desconectado do Discord")

@bot.event
async def on_resumed():
    """Evento quando o bot reconecta"""
    logging.info("🔄 Bot reconectado ao Discord")

@bot.command()
@commands.has_permissions(administrator=True)
async def talk(ctx, *, mensagem):
    """Comando para enviar mensagem em outro canal (apenas admins)"""
    try:
        # Verificar se está no canal correto
        if ctx.channel.id != DISCORD_NEW_MEMBER_CHANNEL_ID:
            await ctx.message.delete()
            await ctx.send(f"❌ Este comando só pode ser usado em <#{DISCORD_NEW_MEMBER_CHANNEL_ID}>.", delete_after=10)
            return

        # Deletar mensagem original
        await ctx.message.delete()

        # Obter canal de destino
        canal_anuncios = bot.get_channel(DISCORD_ANNOUNCEMENT_CHANNEL_ID)
        if not canal_anuncios:
            await ctx.send("❌ Canal de anúncios não encontrado.", delete_after=10)
            logging.error(f"Canal de anúncios não encontrado: {DISCORD_ANNOUNCEMENT_CHANNEL_ID}")
            return

        # Verificar permissões
        if not canal_anuncios.permissions_for(ctx.guild.me).send_messages:
            await ctx.send("❌ Bot sem permissão para enviar no canal de anúncios.", delete_after=10)
            logging.error(f"Bot sem permissão no canal: {DISCORD_ANNOUNCEMENT_CHANNEL_ID}")
            return

        # Enviar mensagem
        await canal_anuncios.send(mensagem)
        await ctx.send("✅ Mensagem enviada com sucesso!", delete_after=10)
        logging.info(f"✅ Mensagem enviada via /talk por {ctx.author.name}: '{mensagem}'")
        
    except discord.Forbidden:
        await ctx.send("❌ Bot sem permissões suficientes.", delete_after=10)
        logging.error(f"Permissões insuficientes para /talk por {ctx.author.name}")
    except Exception as e:
        await ctx.send(f"❌ Erro: {str(e)}", delete_after=10)
        logging.error(f"Erro no comando /talk: {e}")

@talk.error
async def talk_error(ctx, error):
    """Tratamento de erro para o comando talk"""
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Apenas administradores podem usar `/talk`.", delete_after=10)
        logging.warning(f"Usuário {ctx.author.name} tentou usar /talk sem permissões")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Uso: `/talk <mensagem>`. Exemplo: `/talk Olá comunidade!`", delete_after=10)
    else:
        await ctx.send(f"❌ Erro inesperado: {str(error)}", delete_after=10)
        logging.error(f"Erro inesperado no /talk: {error}")

@bot.command()
async def ping(ctx):
    """Comando de teste para verificar se o bot está funcionando"""
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Latência: {latency}ms")

@bot.command()
async def gm(ctx):
    """Comando para enviar GM manualmente"""
    if ctx.author.guild_permissions.administrator:
        await enviar_gm_discord()
        await ctx.send("✅ GM enviado manualmente!")
    else:
        await ctx.send("❌ Apenas administradores podem usar `/gm`.")

@bot.command()
async def status(ctx):
    """Comando para verificar status do bot"""
    embed = discord.Embed(title="🤖 Status do Bot", color=0x00ff00)
    embed.add_field(name="Status", value="✅ Online", inline=True)
    embed.add_field(name="Latência", value=f"🏓 {round(bot.latency * 1000)}ms", inline=True)
    embed.add_field(name="Servidores", value=f"🏠 {len(bot.guilds)}", inline=True)
    embed.add_field(name="GM Diário", value="⏰ 09:00 UTC", inline=True)
    embed.add_field(name="Canal GM", value=f"<#{DISCORD_GM_CHANNEL_ID}>", inline=True)
    embed.add_field(name="Canal Talk", value=f"<#{DISCORD_NEW_MEMBER_CHANNEL_ID}>", inline=True)
    
    await ctx.send(embed=embed)

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        logging.error("❌ DISCORD_TOKEN não encontrado no arquivo .env")
        exit(1)
    
    logging.info("🚀 Iniciando Bot BL4CL4 - Versão Render")
    
    # Iniciar threads em background
    threading.Thread(target=run_flask, daemon=True).start()
    threading.Thread(target=agendador, daemon=True).start()
    threading.Thread(target=keep_alive, daemon=True).start()
    
    # Executar o bot
    bot.run(DISCORD_TOKEN) 