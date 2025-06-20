import os
import discord
from discord.ext import commands
import schedule
import time
import threading
from dotenv import load_dotenv
import asyncio
import logging
import json
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

# Configurações Discord
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_GM_CHANNEL_ID = int(os.getenv("DISCORD_GM_CHANNEL_ID") or 0)
DISCORD_NEW_MEMBER_CHANNEL_ID = 1378199753484926976      # Canal onde o comando /talk é usado
DISCORD_ANNOUNCEMENT_CHANNEL_ID = 1333169997228281978    # Canal de destino para o comando /talk

# --- Sistema de Moeda (VALs) ---
SALDOS_FILE = "saldos.json"
NOME_MOEDA = "VALs"
GANHO_POR_MSG = 1
COOLDOWN_MSG = 60  # em segundos

user_cooldowns = {}

def carregar_saldos():
    """Carrega os saldos do arquivo JSON."""
    if not os.path.exists(SALDOS_FILE):
        return {}
    try:
        with open(SALDOS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def salvar_saldos(saldos):
    """Salva os saldos no arquivo JSON."""
    with open(SALDOS_FILE, 'w') as f:
        json.dump(saldos, f, indent=4)

saldos = carregar_saldos()

# Função para carregar GMs do arquivo tweets.txt
def carregar_gms_do_arquivo():
    gms = []
    try:
        with open("tweets.txt", "r", encoding="utf-8") as f:
            conteudo = f.read()
            blocos = conteudo.split("\n\n")
            for bloco in blocos:
                bloco = bloco.strip()
                if bloco:
                    gms.append(bloco)
    except FileNotFoundError:
        logging.warning("⚠️ Arquivo tweets.txt não encontrado.")
    return gms

gms_prontos = carregar_gms_do_arquivo()

# Função para pegar o GM do dia baseado no dia do mês
def gm_do_dia():
    if not gms_prontos:
        logging.warning("⚠️ Nenhum GM encontrado no arquivo.")
        return None
    import datetime
    dia = datetime.datetime.utcnow().day
    indice = (dia - 1) % len(gms_prontos)
    logging.info(f"Selecionando GM do dia: índice {indice}")
    return gms_prontos[indice]

# Configurar bot Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Enviar mensagem GM no Discord
async def enviar_gm_valoris_discord():
    mensagem = gm_do_dia() or "GM from Valoris"
    channel = bot.get_channel(DISCORD_GM_CHANNEL_ID)
    if channel:
        await channel.send(mensagem)
        logging.info(f"Mensagem GM enviada no Discord: {mensagem}")
    else:
        logging.error("❌ Canal Discord para GM não encontrado")

def agendar_gm_discord():
    asyncio.run_coroutine_threadsafe(enviar_gm_valoris_discord(), bot.loop)

# Agendar tarefas
schedule.every().day.at("09:00").do(agendar_gm_discord)

# Thread para rodar o agendador em background
def agendador():
    while True:
        logging.info(f"Horário atual UTC: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}")
        schedule.run_pending()
        time.sleep(60)

threading.Thread(target=agendador, daemon=True).start()

@bot.event
async def on_ready():
    logging.info(f"🤖 Bot Discord conectado como {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    author_id = str(message.author.id)
    current_time = time.time()

    # Cooldown para ganho de VALs
    if author_id in user_cooldowns and current_time - user_cooldowns[author_id] < COOLDOWN_MSG:
        await bot.process_commands(message)
        return
        
    user_cooldowns[author_id] = current_time

    # Adicionar VALs
    saldos[author_id] = saldos.get(author_id, 0) + GANHO_POR_MSG
    salvar_saldos(saldos)
    
    # É crucial para que os outros comandos continuem funcionando
    await bot.process_commands(message)

# Comando /talk para enviar mensagem em um canal específico
@bot.command()
@commands.has_permissions(administrator=True)
async def talk(ctx, *, mensagem):
    """Envia uma mensagem do canal de comando para o canal de anúncios."""
    if ctx.channel.id != DISCORD_NEW_MEMBER_CHANNEL_ID:
        await ctx.message.delete()
        await ctx.send(f"Este comando só pode ser usado em <#{DISCORD_NEW_MEMBER_CHANNEL_ID}>.", delete_after=10)
        return

    await ctx.message.delete()

    canal_anuncios = bot.get_channel(DISCORD_ANNOUNCEMENT_CHANNEL_ID)
    if canal_anuncios:
        try:
            await canal_anuncios.send(mensagem)
            await ctx.send(f"✅ Mensagem enviada para {canal_anuncios.mention}.", delete_after=10)
            logging.info(f"Mensagem enviada via /talk por {ctx.author.name}: '{mensagem}'")
        except Exception as e:
            await ctx.send(f"❌ Ocorreu um erro ao enviar a mensagem: {e}", delete_after=10)
            logging.error(f"Erro no comando /talk: {e}")
    else:
        await ctx.send("❌ Canal de anúncios não encontrado. Verifique o ID.", delete_after=10)
        logging.warning(f"Canal de anúncios ({DISCORD_ANNOUNCEMENT_CHANNEL_ID}) não encontrado ao usar /talk.")

# --- Comandos da Moeda ---

@bot.command(name="saldo", aliases=["val", "vals", "balance"])
async def saldo(ctx, membro: discord.Member = None):
    """Verifica o saldo de VALs de um membro."""
    if membro is None:
        membro = ctx.author

    saldo_membro = saldos.get(str(membro.id), 0)
    await ctx.send(f"**{membro.display_name}** possui **{saldo_membro} {NOME_MOEDA}**.")

@bot.command(name="rank", aliases=["leaderboard"])
async def rank(ctx):
    """Mostra o ranking dos membros com mais VALs."""
    if not saldos:
        await ctx.send("Ninguém possui VALs ainda. Comece a conversar!")
        return

    # Ordena os saldos do maior para o menor
    sorted_saldos = sorted(saldos.items(), key=lambda item: item[1], reverse=True)

    embed = discord.Embed(title=f"🏆 Ranking de {NOME_MOEDA}", color=0x1a1a1a)
    
    rank_text = ""
    for i, (user_id, saldo_val) in enumerate(sorted_saldos[:10]): # Pega os top 10
        try:
            membro = await ctx.guild.fetch_member(int(user_id))
            nome_membro = membro.display_name
        except discord.NotFound:
            nome_membro = f"ID: {user_id}" # Se o membro saiu do servidor

        rank_text += f"**{i+1}.** {nome_membro} - **{saldo_val} {NOME_MOEDA}**\n"

    if not rank_text:
        await ctx.send("Não foi possível gerar o ranking.")
        return

    embed.description = rank_text
    await ctx.send(embed=embed)

keep_alive()
bot.run(DISCORD_TOKEN)
