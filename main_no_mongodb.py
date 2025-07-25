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
from collections import defaultdict
from new_contract_utils import gerar_ranking_holders, analisar_traits, analisar_districts
from discord.ext.commands import has_permissions, CheckFailure

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

# --- Sistema de Moeda (VALs) com arquivo JSON ---
NOME_MOEDA = "VALs"
GANHO_POR_MSG = 1
COOLDOWN_MSG = 60  # em segundos
SALDOS_FILE = "saldos.json"

user_cooldowns = {}

def carregar_saldos():
    """Carrega os saldos do arquivo JSON."""
    try:
        if os.path.exists(SALDOS_FILE):
            with open(SALDOS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except Exception as e:
        logging.error(f"Erro ao carregar saldos do arquivo: {e}")
        return {}

def salvar_saldos(saldos):
    """Salva os saldos no arquivo JSON."""
    try:
        with open(SALDOS_FILE, 'w', encoding='utf-8') as f:
            json.dump(saldos, f, indent=2, ensure_ascii=False)
        logging.info(f"Salvos {len(saldos)} saldos no arquivo")
    except Exception as e:
        logging.error(f"Erro ao salvar saldos: {e}")

def adicionar_val(user_id, quantidade=1):
    """Adiciona VALs para um usuário específico."""
    try:
        saldos = carregar_saldos()
        if user_id not in saldos:
            saldos[user_id] = 0
        saldos[user_id] += quantidade
        salvar_saldos(saldos)
        logging.info(f"Adicionado {quantidade} VAL para usuário {user_id}")
    except Exception as e:
        logging.error(f"Erro ao adicionar VALs: {e}")

def obter_saldo(user_id):
    """Obtém o saldo de um usuário específico."""
    try:
        saldos = carregar_saldos()
        return saldos.get(user_id, 0)
    except Exception as e:
        logging.error(f"Erro ao obter saldo: {e}")
        return 0

def obter_ranking():
    """Obtém o ranking de todos os usuários."""
    try:
        saldos = carregar_saldos()
        ranking = [{'user_id': user_id, 'saldo': saldo} for user_id, saldo in saldos.items()]
        return sorted(ranking, key=lambda x: x['saldo'], reverse=True)
    except Exception as e:
        logging.error(f"Erro ao obter ranking: {e}")
        return []

# Carregar saldos iniciais
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
    
    # Processar comandos
    await bot.process_commands(message)

@bot.command()
@commands.has_permissions(administrator=True)
async def talk(ctx, *, mensagem):
    """Comando para enviar mensagem em outro canal (apenas admins)"""
    if ctx.channel.id == DISCORD_NEW_MEMBER_CHANNEL_ID:
        channel_destino = bot.get_channel(DISCORD_ANNOUNCEMENT_CHANNEL_ID)
        if channel_destino:
            embed = discord.Embed(
                title="📢 Anúncio da Comunidade",
                description=mensagem,
                color=0x00ff00
            )
            embed.set_footer(text=f"Enviado por {ctx.author.display_name}")
            await channel_destino.send(embed=embed)
            await ctx.send("✅ Mensagem enviada com sucesso!")
        else:
            await ctx.send("❌ Canal de destino não encontrado!")
    else:
        await ctx.send("❌ Este comando só pode ser usado no canal correto!")

@bot.command(name="saldo", aliases=["val", "vals", "balance"])
async def saldo(ctx, membro: discord.Member = None):
    """Mostra o saldo de VALs do usuário ou de outro membro"""
    if membro is None:
        membro = ctx.author
    
    saldo_membro = obter_saldo(str(membro.id))
    
    embed = discord.Embed(
        title=f"💰 Saldo de {NOME_MOEDA}",
        description=f"**{membro.display_name}** tem **{saldo_membro} {NOME_MOEDA}**",
        color=0x00ff00
    )
    embed.set_thumbnail(url=membro.avatar.url if membro.avatar else membro.default_avatar.url)
    
    await ctx.send(embed=embed)

@bot.command(name="posicao", aliases=["rank", "leaderboard"])
async def posicao(ctx):
    """Mostra o ranking de VALs"""
    ranking = obter_ranking()
    
    if not ranking:
        await ctx.send("📊 Nenhum usuário encontrado no ranking!")
        return
    
    # Encontrar posição do usuário atual
    user_id = str(ctx.author.id)
    posicao_usuario = None
    for i, item in enumerate(ranking, 1):
        if item['user_id'] == user_id:
            posicao_usuario = i
            break
    
    embed = discord.Embed(
        title=f"🏆 Ranking de {NOME_MOEDA}",
        color=0xffd700
    )
    
    # Top 10
    for i, item in enumerate(ranking[:10], 1):
        try:
            user = await bot.fetch_user(int(item['user_id']))
            nome = user.display_name
        except:
            nome = f"Usuário {item['user_id']}"
        
        medalha = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"#{i}"
        embed.add_field(
            name=f"{medalha} {nome}",
            value=f"**{item['saldo']} {NOME_MOEDA}**",
            inline=False
        )
    
    if posicao_usuario:
        embed.set_footer(text=f"Sua posição: #{posicao_usuario}")
    
    await ctx.send(embed=embed)

@bot.command(name="rankingholders")
# @commands.has_permissions(administrator=True)  # Comentado temporariamente
async def rankingholders(ctx):
    """Mostra o ranking dos holders do novo contrato NFT"""
    try:
        await ctx.send("🔄 Buscando dados dos holders...")
        
        # Gerar ranking usando a função do new_contract_utils
        ranking_data = gerar_ranking_holders()
        
        if not ranking_data:
            await ctx.send("❌ Erro ao buscar dados dos holders!")
            return
        
        embed = discord.Embed(
            title="🏆 Ranking dos Holders - Novo Contrato",
            description="Top holders do contrato KT1JhZBNxoMB3QzcdJfopmq3R5R6jPiwC1nw",
            color=0x00ff00
        )
        
        # Mostrar top 10
        for i, holder in enumerate(ranking_data[:10], 1):
            medalha = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"#{i}"
            embed.add_field(
                name=f"{medalha} {holder['address'][:8]}...{holder['address'][-6:]}",
                value=f"**{holder['balance']} NFTs**",
                inline=False
            )
        
        embed.set_footer(text=f"Total de holders: {len(ranking_data)}")
        embed.timestamp = discord.utils.utcnow()
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        logging.error(f"Erro no comando rankingholders: {e}")
        await ctx.send(f"❌ Erro ao gerar ranking: {str(e)}")

@bot.command(name="darvals")
@commands.has_permissions(administrator=True)
async def darvals(ctx, membro: discord.Member, quantidade: int):
    """Dá VALs para um membro (apenas admins)"""
    if quantidade <= 0:
        await ctx.send("❌ Quantidade deve ser maior que 0!")
        return
    
    adicionar_val(str(membro.id), quantidade)
    
    embed = discord.Embed(
        title="💰 VALs Adicionados",
        description=f"**{quantidade} {NOME_MOEDA}** adicionados para **{membro.display_name}**",
        color=0x00ff00
    )
    embed.set_footer(text=f"Adicionado por {ctx.author.display_name}")
    
    await ctx.send(embed=embed)

# Comando de admin para dar VALs para qualquer usuário
@bot.command(name="darval")
@has_permissions(administrator=True)
async def darval(ctx, user_id: str, quantidade: int):
    """Dá VALs para qualquer usuário (apenas admins)"""
    try:
        if quantidade <= 0:
            await ctx.send("❌ Quantidade deve ser maior que zero.")
            return
        # Carregar saldos
        if os.path.exists("saldos.json"):
            with open("saldos.json", "r", encoding="utf-8") as f:
                saldos = json.load(f)
        else:
            saldos = {}
        # Atualizar saldo
        saldos[user_id] = saldos.get(user_id, 0) + quantidade
        with open("saldos.json", "w", encoding="utf-8") as f:
            json.dump(saldos, f, indent=2, ensure_ascii=False)
        await ctx.send(f"✅ {quantidade} VAL(s) adicionado(s) para o usuário `{user_id}`. Novo saldo: {saldos[user_id]}")
        logging.info(f"Admin {ctx.author.id} deu {quantidade} VALs para {user_id}")
    except Exception as e:
        await ctx.send(f"❌ Erro ao dar VALs: {e}")
        logging.error(f"Erro no comando darval: {e}")

@darval.error
async def darval_error(ctx, error):
    if isinstance(error, CheckFailure):
        await ctx.send("❌ Você não tem permissão para usar este comando.")
    else:
        await ctx.send(f"❌ Erro: {error}")


# Comando para mostrar traits dos NFTs
@bot.command(name="traits")
async def traits(ctx):
    """Mostra a lista de traits dos NFTs com percentuais"""
    try:
        await ctx.send("🔍 **Buscando traits dos NFTs...**")
        
        traits_data = analisar_traits()
        
        if not traits_data:
            await ctx.send("❌ Não foi possível buscar os traits dos NFTs.")
            return
        
        embed = discord.Embed(
            title="🎨 **Traits dos NFTs - Balaclava System**",
            description="Estatísticas dos traits encontrados na coleção",
            color=0x00ff00
        )
        
        for trait_category, traits in traits_data.items():
            # Ordenar traits por percentual (mais raros primeiro)
            sorted_traits = sorted(traits.items(), key=lambda x: x[1]['percentage'])
            
            trait_text = ""
            for trait_value, stats in sorted_traits:
                count = stats['count']
                percentage = stats['percentage']
                rarity_emoji = "💎" if percentage < 5 else "🔥" if percentage < 15 else "⭐" if percentage < 30 else "📊"
                trait_text += f"{rarity_emoji} **{trait_value}**: {count} ({percentage}%)\n"
            
            if trait_text:
                # Limitar tamanho do campo (Discord tem limite de 1024 caracteres)
                if len(trait_text) > 1024:
                    trait_text = trait_text[:1021] + "..."
                
                embed.add_field(
                    name=f"🎭 {trait_category}",
                    value=trait_text,
                    inline=False
                )
        
        embed.set_footer(text="💎 Raros | 🔥 Especiais | ⭐ Comuns | 📊 Muito Comuns")
        await ctx.send(embed=embed)
        
    except Exception as e:
        logging.error(f"Erro no comando traits: {e}")
        await ctx.send("❌ Erro ao buscar traits. Tente novamente.")


# Comando para mostrar Districts e membros
@bot.command(name="districts")
async def districts(ctx):
    """Mostra os Districts e quantidade de membros em cada um"""
    try:
        await ctx.send("🏘️ **Buscando Districts e membros...**")
        
        districts_data = analisar_districts()
        
        if not districts_data:
            await ctx.send("❌ Não foi possível buscar os Districts.")
            return
        
        embed = discord.Embed(
            title="🏘️ **Districts - Balaclava System**",
            description="Distribuição de membros por District",
            color=0x00ff00
        )
        
        # Ordenar districts por número de membros únicos (maior primeiro)
        sorted_districts = sorted(districts_data.items(), key=lambda x: x[1]['unique_members'], reverse=True)
        
        for district_name, stats in sorted_districts:
            count = stats['count']
            percentage = stats['percentage']
            unique_members = stats['unique_members']
            
            # Emoji baseado no tamanho do district
            district_emoji = "🏙️" if unique_members > 50 else "🏘️" if unique_members > 20 else "🏠" if unique_members > 10 else "🏡"
            
            district_text = f"{district_emoji} **{district_name}**\n"
            district_text += f"👥 **Membros únicos**: {unique_members}\n"
            district_text += f"🎭 **Total NFTs**: {count}\n"
            district_text += f"📊 **Percentual**: {percentage}%\n"
            
            embed.add_field(
                name=f"🏘️ {district_name}",
                value=district_text,
                inline=True
            )
        
        # Adicionar estatísticas gerais
        total_members = sum(stats['unique_members'] for stats in districts_data.values())
        total_nfts = sum(stats['count'] for stats in districts_data.values())
        
        embed.add_field(
            name="📈 **Estatísticas Gerais**",
            value=f"👥 **Total de membros únicos**: {total_members}\n🎭 **Total de NFTs**: {total_nfts}\n🏘️ **Districts encontrados**: {len(districts_data)}",
            inline=False
        )
        
        embed.set_footer(text="🏙️ Grande | 🏘️ Médio | 🏠 Pequeno | 🏡 Muito Pequeno")
        await ctx.send(embed=embed)
        
    except Exception as e:
        logging.error(f"Erro no comando districts: {e}")
        await ctx.send("❌ Erro ao buscar Districts. Tente novamente.")


# Iniciar servidor Flask para keep-alive
keep_alive()

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN) 