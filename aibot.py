import discord
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do arquivo .env

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # necessário para ler o conteúdo das mensagens

client = discord.Client(intents=intents)

CANAL_SOLICITACAO = 1378199753484926976  # canal onde o bot ouve "NOVO MEMBRO"
CANAL_REGISTRO = 1378564229061415023    # canal onde o bot salva os membros aprovados

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.id == CANAL_SOLICITACAO:
        if message.content.upper() == "NOVO MEMBRO":
            await message.channel.send(f"{message.author.mention}, pedido de novo membro recebido! Aguarde aprovação.")

client.run(TOKEN)
