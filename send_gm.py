import os
import discord
import asyncio
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_GM_CHANNEL_ID = int(os.getenv("DISCORD_GM_CHANNEL_ID"))

async def enviar_gm():
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        channel = client.get_channel(DISCORD_GM_CHANNEL_ID)
        if channel:
            await channel.send("GM from Valoris")
            print("Mensagem enviada com sucesso!")
        else:
            print("Canal Discord para GM não encontrado")
        await client.close()

    await client.start(DISCORD_TOKEN)

asyncio.run(enviar_gm())
