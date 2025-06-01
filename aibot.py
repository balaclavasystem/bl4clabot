import discord
from discord.ext import commands
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
NEW_MEMBER_CHANNEL_ID = 1378199753484926976
APPROVED_MEMBERS_CHANNEL_ID = 1378564229061415023

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

def generate_member_profile(description):
    prompt = f"""
You are creating a member profile for the fictional city of Valoris. Use the following description provided by the user to generate a profile.

Description: "{description}"

Respond in this exact structure (and only this), in English:

Name: [First and Last Name]
Age: [Number between 21 and 55]
District: [Choose a district based on the description, or invent one]
Member since: [Year]

Bio:
[A short, creative, mysterious description of the character within Valoris. Max 3 short paragraphs.]
"""

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
    )

    return response.choices[0].message.content.strip()

@bot.event
async def on_ready():
    print(f"🤖 AIBOT online como {bot.user}")

@bot.command()
async def newmember(ctx, *, descricao):
    if ctx.channel.id != NEW_MEMBER_CHANNEL_ID:
        await ctx.send("⛔ Esse comando só pode ser usado no canal de criação de membros.")
        return

    try:
        await ctx.send("🧠 Gerando perfil do membro...")
        profile = generate_member_profile(descricao)
        await ctx.send(f"✅ Perfil gerado:\n\n{profile}")

        await ctx.send("📌 Se aprovado, digite `/aprovar` para mover o perfil ao canal oficial.")
        # Salva o perfil no contexto do autor para uso posterior
        bot.last_profile = profile
        bot.last_author = ctx.author.id

    except Exception as e:
        print(f"Erro ao gerar perfil: {e}")
        await ctx.send("❌ Error generating profile. Check logs.")

@bot.command()
async def aprovar(ctx):
    if ctx.channel.id != NEW_MEMBER_CHANNEL_ID:
        await ctx.send("⛔ Esse comando só pode ser usado no canal de criação de membros.")
        return

    if not hasattr(bot, "last_profile") or ctx.author.id != bot.last_author:
        await ctx.send("⚠️ Nenhum perfil recente encontrado ou você não é o autor.")
        return

    canal_destino = bot.get_channel(APPROVED_MEMBERS_CHANNEL_ID)
    if canal_destino:
        await canal_destino.send(bot.last_profile)
        await ctx.send("✅ Perfil aprovado e movido para o canal oficial.")
    else:
        await ctx.send("❌ Erro: canal de destino não encontrado.")

bot.run(os.getenv("DISCORD_TOKEN"))
