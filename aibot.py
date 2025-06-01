import os
import discord
from discord.ext import commands
import openai
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

openai.api_key = OPENAI_API_KEY

# IDs dos canais
INPUT_CHANNEL_ID = 1378199753484926976
OUTPUT_CHANNEL_ID = 1378564229061415023

# Configurações do bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Prompt base do projeto
BALACLAVA_PROMPT = """
Você está assumindo o papel de consultor criativo, estrategista Web3 e narrador visual do universo chamado Balaclava System.
[COLE TODO O SEU PROMPT AQUI, SEM CORTES]
"""

# Comando: /newmember descrição
@bot.command(name='newmember')
async def new_member(ctx, *, description):
    if ctx.channel.id != INPUT_CHANNEL_ID:
        return  # Ignora se não for no canal correto

    full_prompt = f"""{BALACLAVA_PROMPT}

Com base na seguinte descrição, gere um novo perfil de personagem:

Descrição: {description}

Formato:
Name: [nome fictício coerente com o universo]
Age: [idade entre 18 e 60]

Bio:
[Texto descritivo seguindo o estilo do Balaclava System, em inglês]
"""

    try:
        await ctx.send("🔄 Gerando novo membro...")

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um escritor criativo especialista em universos de ficção."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.8
        )

        profile = response['choices'][0]['message']['content']

        await ctx.send(f"🆕 New Member Profile Generated:\n```{profile}```\n✅ Se estiver OK, digite `/approve`.")

        bot.last_profile = {
            'author': ctx.author.id,
            'content': profile
        }

    except Exception as e:
        await ctx.send(f"❌ Erro ao gerar perfil: {e}")

# Comando: /approve
@bot.command(name='approve')
async def approve(ctx):
    if not hasattr(bot, 'last_profile'):
        await ctx.send("❌ Nenhum perfil pendente de aprovação.")
        return

    if bot.last_profile['author'] != ctx.author.id:
        await ctx.send("❌ Apenas quem criou o perfil pode aprovar.")
        return

    try:
        output_channel = bot.get_channel(OUTPUT_CHANNEL_ID)
        if output_channel:
            await output_channel.send(f"📢 NEW MEMBER:\n```{bot.last_profile['content']}```")
            await ctx.send("✅ Perfil aprovado e publicado.")
            del bot.last_profile
        else:
            await ctx.send("❌ Canal de destino não encontrado.")

    except Exception as e:
        await ctx.send(f"❌ Erro ao publicar o perfil: {e}")

# Roda o bot
bot.run(DISCORD_TOKEN)
