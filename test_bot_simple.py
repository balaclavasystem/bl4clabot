#!/usr/bin/env python3
"""
Versão simplificada do bot para testar apenas o comando rankingholders
"""
import os
import discord
from discord.ext import commands
import logging
import requests
from new_contract_utils import gerar_ranking_holders
from dotenv import load_dotenv

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

if not DISCORD_TOKEN or DISCORD_TOKEN == "seu_token_real_do_discord":
    print("❌ ERRO: Token do Discord não configurado!")
    print("Edite o arquivo .env e configure DISCORD_TOKEN=seu_token_real_aqui")
    exit(1)

# Configurar bot Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    logging.info(f"🤖 Bot Discord conectado como {bot.user}")
    print(f"✅ Bot conectado como {bot.user}")
    print(f"✅ Use /rankingholders para testar")

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@bot.command(name="rankingvaloris")
async def rankingvaloris(ctx):
    """Mostra o ranking real dos holders do novo contrato on-chain."""
    try:
        print(f"🔍 Comando /rankingholders executado por {ctx.author.name}")
        logging.info(f"Comando /rankingholders executado por {ctx.author.name}")
        
        await ctx.message.delete()
        await ctx.send("🔍 Buscando ranking on-chain do novo contrato...", delete_after=5)
        
        # Gerar ranking usando a função do novo arquivo
        ranking, total_holders, total_nfts = gerar_ranking_holders()

        if not ranking:
            await ctx.send("❌ Nenhum holder com balance > 0 encontrado.", delete_after=10)
            return

        # Criar embed
        embed = discord.Embed(title="🏆 Ranking On-chain - Novo Contrato", color=0x1a1a1a)
        description = ""
        for i, (address, alias, balance, tokens) in enumerate(ranking[:20], 1):
            name = f"{alias} ({address})" if alias else address
            description += f"**{i}.** `{name}` - **{balance} NFTs**\n"
            
            # Mostrar detalhes dos tokens se houver mais de 1
            if len(tokens) > 1:
                for token in tokens:
                    description += f"   └─ {token['name']} (ID: {token['token_id']})\n"
        
        description += f"\n**Total únicos:** {total_holders} | **Total NFTs:** {total_nfts}"
        embed.description = description
        
        await ctx.send(embed=embed)
        logging.info(f"Ranking on-chain do novo contrato enviado com sucesso por {ctx.author.name}")
        print(f"✅ Ranking enviado com sucesso!")
        
    except requests.RequestException as e:
        error_msg = f"❌ Erro de conexão com TzKT API: {e}"
        await ctx.send(error_msg, delete_after=15)
        logging.error(f"Erro de API no /rankingholders: {e}")
        print(f"❌ Erro de API: {e}")
        
    except Exception as e:
        error_msg = f"❌ Erro inesperado: {e}"
        await ctx.send(error_msg, delete_after=15)
        logging.error(f"Erro inesperado no /rankingholders: {e}")
        print(f"❌ Erro inesperado: {e}")

@bot.command(name="test")
async def test(ctx):
    """Comando de teste simples."""
    await ctx.send("✅ Bot funcionando!")

print("🚀 Iniciando bot simplificado...")
print("📝 Logs serão salvos em bot.log")
bot.run(DISCORD_TOKEN) 