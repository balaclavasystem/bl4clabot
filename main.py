import os
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

# Configurações Discord
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID") or 0)               # Canal para notificações gerais
DISCORD_GM_CHANNEL_ID = int(os.getenv("DISCORD_GM_CHANNEL_ID") or 0)         # Canal para mensagem fixa GM
DISCORD_NEW_MEMBER_CHANNEL_ID = 1378199753484926976                      # Canal onde o usuário envia NEW MEMBER para revisão
DISCORD_APPROVED_MEMBER_CHANNEL_ID = 1378564229061415023                 # Canal onde será salvo perfil aprovado
DISCORD_ANNOUNCEMENT_CHANNEL_ID = 1333169997228281978                    # Canal de anúncios para o comando /talk

# Configurar cliente OpenAI (API >= 1.0.0)
client_openai = OpenAI()

# Função para carregar GMs do arquivo tweets.txt
def carregar_gms_do_arquivo():
    gms = []
    try:
        with open("tweets.txt", "r", encoding="utf-8") as f:
            conteudo = f.read()
            blocos = conteudo.split("\n\n")  # separa por linhas vazias
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

# Enviar mensagem em canal Discord (para notificações)
async def enviar_mensagem_discord(mensagem):
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send(mensagem)
        logging.info(f"Mensagem enviada no Discord: {mensagem}")
    else:
        logging.error("❌ Canal Discord para notificações não encontrado")

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
schedule.every().day.at("09:00").do(agendar_gm_discord)      # Mensagem fixa no Discord às 09:00 UTC

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

async def adaptar_frase_openai(frase):
    """Pede para a OpenAI adaptar uma frase ao tom de voz do Balaclava System."""
    prompt = f"""
You are a creative assistant for the Balaclava System project, known for a poetic, urban, and mysterious tone.
Rewrite the following phrase to fit this style. Keep the core meaning intact but transform the delivery.
Respond ONLY with the adapted phrase itself.

Original phrase: "{frase}"
"""
    try:
        response = client_openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a creative writing assistant for the Balaclava System."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        frase_adaptada = response.choices[0].message.content.strip()
        return frase_adaptada
    except Exception as e:
        logging.error(f"Erro ao adaptar frase com OpenAI: {e}")
        return None

@bot.event
async def on_ready():
    logging.info(f"🤖 Bot Discord conectado como {bot.user}")

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
    """Envia uma mensagem para o canal de anúncios, adaptando-a com IA se solicitado."""
    # Verifica se o comando foi usado no canal correto
    if ctx.channel.id != DISCORD_NEW_MEMBER_CHANNEL_ID:
        await ctx.message.delete()
        await ctx.send(f"Este comando só pode ser usado em <#{DISCORD_NEW_MEMBER_CHANNEL_ID}>.", delete_after=10)
        return

    # Deleta a mensagem de comando para manter o canal limpo
    await ctx.message.delete()

    mensagem_final = mensagem
    keyword = "adapte a frase:"

    if mensagem.lower().startswith(keyword):
        frase_original = mensagem[len(keyword):].strip()
        if not frase_original:
            await ctx.send("⚠️ Por favor, forneça uma frase para adaptar.", delete_after=10)
            return

        aviso_ia = await ctx.send("🧠 Adaptando a frase com a IA...", delete_after=15)
        
        frase_adaptada = await adaptar_frase_openai(frase_original)
        
        await aviso_ia.delete() # Deleta o aviso de "adaptando"

        if frase_adaptada:
            mensagem_final = frase_adaptada
        else:
            await ctx.send("❌ Não foi possível adaptar a frase. Verifique os logs.", delete_after=10)
            return

    canal_anuncios = bot.get_channel(DISCORD_ANNOUNCEMENT_CHANNEL_ID)
    if canal_anuncios:
        try:
            await canal_anuncios.send(mensagem_final)
            # Envia uma confirmação temporária
            await ctx.send(f"✅ Mensagem enviada para {canal_anuncios.mention}.", delete_after=10)
            logging.info(f"Mensagem enviada via /talk por {ctx.author.name}: '{mensagem_final}'")
        except Exception as e:
            await ctx.send(f"❌ Ocorreu um erro ao enviar a mensagem: {e}", delete_after=10)
            logging.error(f"Erro no comando /talk: {e}")
    else:
        await ctx.send("❌ Canal de anúncios não encontrado. Verifique o ID.", delete_after=10)
        logging.warning(f"Canal de anúncios ({DISCORD_ANNOUNCEMENT_CHANNEL_ID}) não encontrado ao usar /talk.")

keep_alive()
bot.run(DISCORD_TOKEN)
