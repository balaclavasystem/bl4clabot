import os
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

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Canal para enviar a mensagem "GM from Valoris"
DISCORD_GM_CHANNEL_ID = int(os.getenv("DISCORD_GM_CHANNEL_ID"))

# Configurar bot Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

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

# Agendar tarefa diária do GM
schedule.every().day.at("12:00").do(agendar_gm_discord)  # Ajuste o horário aqui (UTC)

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

bot.run(DISCORD_TOKEN)
