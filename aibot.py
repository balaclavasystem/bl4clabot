import discord
from discord.ext import commands
import os
import openai
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

REVIEW_CHANNEL_ID = 1378199753484926976
APPROVED_CHANNEL_ID = 1378564229061415023

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 AIBot conectado como {bot.user}")

# Comando para criar novo membro
@bot.command()
async def newmember(ctx, *, descricao):
    await ctx.send("🧠 Generating member profile...")
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a creative writer creating character profiles for the fictional city of Valoris."},
                {"role": "user", "content": f"Crie um perfil no formato abaixo, baseado na descrição: {descricao}\n\nFormato:\nName\nAge\nDistrict\nMember since\n\nBio:\n[Texto criativo e misterioso sobre o personagem, com o tom do universo Valoris]"}
            ]
        )

        content = response.choices[0].message.content.strip()
        canal_revisao = bot.get_channel(REVIEW_CHANNEL_ID)
        if canal_revisao:
            await canal_revisao.send(f"🆕 Novo Membro Sugerido:\n\n{content}")
            await ctx.send("✅ Perfil gerado e enviado para revisão.")
        else:
            await ctx.send("❌ Canal de revisão não encontrado.")

    except Exception as e:
        await ctx.send(f"❌ Erro ao gerar perfil: {e}")

# Comando para aprovar e enviar o perfil ao canal final
@bot.command()
async def approve(ctx, mensagem_id: int):
    try:
        canal_revisao = bot.get_channel(REVIEW_CHANNEL_ID)
        canal_final = bot.get_channel(APPROVED_CHANNEL_ID)

        mensagem = await canal_revisao.fetch_message(mensagem_id)
        if mensagem and canal_final:
            await canal_final.send(mensagem.content)
            await ctx.send("✅ Perfil aprovado e movido para o canal final.")
        else:
            await ctx.send("❌ Não foi possível mover a mensagem.")

    except Exception as e:
        await ctx.send(f"❌ Erro ao aprovar perfil: {e}")
