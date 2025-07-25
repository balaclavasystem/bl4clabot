#!/usr/bin/env python3
"""
Script para testar especificamente o comando /talk
"""

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Configurações
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_NEW_MEMBER_CHANNEL_ID = 1378199753484926976
DISCORD_ANNOUNCEMENT_CHANNEL_ID = 1333169997228281978

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Bot conectado como {bot.user}")
    print(f"🆔 ID do bot: {bot.user.id}")
    
    # Verificar se o bot está em algum servidor
    if bot.guilds:
        guild = bot.guilds[0]
        print(f"🏠 Servidor: {guild.name}")
        print(f"🆔 ID do servidor: {guild.id}")
        
        # Verificar permissões do bot
        bot_member = guild.get_member(bot.user.id)
        if bot_member:
            print(f"👑 Cargos do bot: {[role.name for role in bot_member.roles]}")
            print(f"🔑 Permissões do bot: {bot_member.guild_permissions}")
        
        # Verificar canais
        new_member_channel = bot.get_channel(DISCORD_NEW_MEMBER_CHANNEL_ID)
        announcement_channel = bot.get_channel(DISCORD_ANNOUNCEMENT_CHANNEL_ID)
        
        if new_member_channel:
            print(f"✅ Canal de comando encontrado: {new_member_channel.name}")
            permissions = new_member_channel.permissions_for(bot_member)
            print(f"📝 Permissões no canal de comando: {permissions.send_messages}")
        else:
            print(f"❌ Canal de comando não encontrado: {DISCORD_NEW_MEMBER_CHANNEL_ID}")
        
        if announcement_channel:
            print(f"✅ Canal de anúncios encontrado: {announcement_channel.name}")
            permissions = announcement_channel.permissions_for(bot_member)
            print(f"📝 Permissões no canal de anúncios: {permissions.send_messages}")
        else:
            print(f"❌ Canal de anúncios não encontrado: {DISCORD_ANNOUNCEMENT_CHANNEL_ID}")
    else:
        print("❌ Bot não está em nenhum servidor")

@bot.command()
@commands.has_permissions(administrator=True)
async def talk(ctx, *, mensagem):
    """Comando de teste para /talk"""
    print(f"🔍 Testando comando /talk...")
    print(f"👤 Usuário: {ctx.author.name}")
    print(f"📝 Mensagem: {mensagem}")
    print(f"📺 Canal: {ctx.channel.name} (ID: {ctx.channel.id})")
    
    try:
        # Verificar canal
        if ctx.channel.id != DISCORD_NEW_MEMBER_CHANNEL_ID:
            await ctx.send(f"❌ Comando deve ser usado em <#{DISCORD_NEW_MEMBER_CHANNEL_ID}>")
            return
        
        # Verificar canal de destino
        canal_anuncios = bot.get_channel(DISCORD_ANNOUNCEMENT_CHANNEL_ID)
        if not canal_anuncios:
            await ctx.send("❌ Canal de anúncios não encontrado")
            return
        
        # Verificar permissões
        bot_member = ctx.guild.get_member(bot.user.id)
        permissions = canal_anuncios.permissions_for(bot_member)
        
        if not permissions.send_messages:
            await ctx.send("❌ Bot sem permissão para enviar no canal de anúncios")
            return
        
        # Enviar mensagem
        await canal_anuncios.send(mensagem)
        await ctx.send("✅ Mensagem enviada com sucesso!")
        print("✅ Teste concluído com sucesso")
        
    except Exception as e:
        await ctx.send(f"❌ Erro: {str(e)}")
        print(f"❌ Erro no teste: {e}")

@talk.error
async def talk_error(ctx, error):
    print(f"❌ Erro no comando talk: {error}")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Você não tem permissão de administrador")
    else:
        await ctx.send(f"❌ Erro: {str(error)}")

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("❌ DISCORD_TOKEN não encontrado no arquivo .env")
        exit(1)
    
    print("🧪 Iniciando teste do comando /talk...")
    bot.run(DISCORD_TOKEN) 