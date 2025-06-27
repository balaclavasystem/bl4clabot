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
import re
import requests
from pymongo import MongoClient

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

# --- Sistema de Moeda (VALs) com MongoDB ---
NOME_MOEDA = "VALs"
GANHO_POR_MSG = 1
COOLDOWN_MSG = 60  # em segundos

# Configuração MongoDB
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGODB_URI)
db = client.bl4clabot
saldos_collection = db.saldos

user_cooldowns = {}

def carregar_saldos():
    """Carrega os saldos do MongoDB."""
    try:
        saldos = {}
        for doc in saldos_collection.find():
            saldos[doc['user_id']] = doc['saldo']
        return saldos
    except Exception as e:
        logging.error(f"Erro ao carregar saldos do MongoDB: {e}")
        return {}

def salvar_saldos(saldos):
    """Salva os saldos no MongoDB."""
    try:
        for user_id, saldo in saldos.items():
            saldos_collection.update_one(
                {'user_id': user_id},
                {'$set': {'saldo': saldo}},
                upsert=True
            )
        logging.info(f"Salvos {len(saldos)} saldos no MongoDB")
    except Exception as e:
        logging.error(f"Erro ao salvar saldos no MongoDB: {e}")

def adicionar_val(user_id, quantidade=1):
    """Adiciona VALs para um usuário específico."""
    try:
        saldos_collection.update_one(
            {'user_id': user_id},
            {'$inc': {'saldo': quantidade}},
            upsert=True
        )
        logging.info(f"Adicionado {quantidade} VAL para usuário {user_id}")
    except Exception as e:
        logging.error(f"Erro ao adicionar VALs: {e}")

def obter_saldo(user_id):
    """Obtém o saldo de um usuário específico."""
    try:
        doc = saldos_collection.find_one({'user_id': user_id})
        return doc['saldo'] if doc else 0
    except Exception as e:
        logging.error(f"Erro ao obter saldo: {e}")
        return 0

def obter_ranking():
    """Obtém o ranking de todos os usuários."""
    try:
        return list(saldos_collection.find().sort('saldo', -1))
    except Exception as e:
        logging.error(f"Erro ao obter ranking: {e}")
        return []

# Carregar saldos iniciais (para compatibilidade)
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

# Thread para manter o bot acordado
def ping_keep_alive():
    while True:
        try:
            # Faz uma requisição para o próprio servidor para mantê-lo acordado
            response = requests.get("http://localhost:8080/health", timeout=5)
            if response.status_code == 200:
                logging.info("✅ Ping de keep-alive realizado com sucesso")
            else:
                logging.warning(f"⚠️ Ping de keep-alive retornou status {response.status_code}")
        except Exception as e:
            logging.error(f"❌ Erro no ping de keep-alive: {e}")
        
        # Pings a cada 10 minutos (600 segundos)
        time.sleep(600)

threading.Thread(target=agendador, daemon=True).start()
threading.Thread(target=ping_keep_alive, daemon=True).start()

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
    adicionar_val(author_id, GANHO_POR_MSG)
    
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

    saldo_membro = obter_saldo(str(membro.id))
    await ctx.send(f"**{membro.display_name}** possui **{saldo_membro} {NOME_MOEDA}**.")

@bot.command(name="posicao", aliases=["rank", "leaderboard"])
async def posicao(ctx):
    """Mostra o ranking dos membros com mais VALs."""
    sorted_saldos = obter_ranking()
    
    if not sorted_saldos:
        await ctx.send("Ninguém possui VALs ainda. Comece a conversar!")
        return

    embed = discord.Embed(title=f"🏆 Ranking de {NOME_MOEDA}", color=0x1a1a1a)
    
    rank_text = ""
    for i, doc in enumerate(sorted_saldos[:10]): # Pega os top 10
        user_id = doc['user_id']
        saldo_val = doc['saldo']
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

@bot.command()
@commands.has_permissions(administrator=True)
async def rankingholders(ctx, *, data: str):
    """Analisa um bloco de texto de atividade e cria um ranking de holders."""
    
    my_username = "@revolue"
    await ctx.message.delete()

    # Keywords para identificar o início de um novo evento na lista
    event_starters = ['Sale', 'Transfer', 'List', 'Mint', 'Burn', 'Auction', 'Offer', 'Cancelled Offer', 'Accepted Offer']
    
    # Padrão de regex para dividir o texto em blocos de transação
    pattern = r'\b(' + '|'.join(event_starters) + r')\b'
    blocks = re.split(pattern, data)
    
    holders = []
    
    # O resultado do split é ['', 'Sale', 'conteúdo do bloco', 'Transfer', 'conteúdo do bloco', ...]
    # Iteramos pelos blocos, pulando de 2 em 2
    for i in range(1, len(blocks), 2):
        event_type = blocks[i]
        event_content = blocks[i+1]
        
        # Processa apenas os eventos de Sale e Transfer, como solicitado
        if event_type in ['Sale', 'Transfer']:
            # Encontra todos os @nomesdeusuario no bloco. Permite letras, números, _ e .
            found_users = re.findall(r'@([\w\.]+)', event_content)
            
            for user in found_users:
                username = '@' + user
                # Adiciona o usuário na lista se não for o admin
                if username.lower() != my_username.lower():
                    holders.append(username)
    
    if not holders:
        await ctx.send("Nenhum holder qualificado encontrado no texto. Verifique se o texto contém transações de 'Sale' ou 'Transfer' com outros usuários.", delete_after=15)
        return
        
    from collections import Counter
    counts = Counter(holders)
    
    # Ordena os holders pela quantidade de NFTs, do maior para o menor
    sorted_holders = counts.most_common()
    
    embed = discord.Embed(title="🏆 Ranking de Holders por Atividade", color=0x1a1a1a)
    
    description = ""
    for i, (username, count) in enumerate(sorted_holders):
        description += f"**{i+1}.** {username} - **{count} NFTs**\n"
        # Limite de segurança para não ultrapassar o máximo de caracteres do Discord
        if len(description) > 3800:
            description += "\n*Ranking truncado para caber na mensagem.*"
            break
            
    embed.description = description
    
    await ctx.send(embed=embed)

keep_alive()
bot.run(DISCORD_TOKEN)
