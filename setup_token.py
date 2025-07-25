#!/usr/bin/env python3
"""
Script para configurar o token do Discord no arquivo .env
"""

import os
import sys

def setup_discord_token():
    print("🔧 Configuração do Token do Discord")
    print("=" * 50)
    
    # Verificar se o arquivo .env existe
    if not os.path.exists('.env'):
        print("❌ Arquivo .env não encontrado!")
        print("Criando arquivo .env...")
        
        # Criar arquivo .env básico
        env_content = """# Token do seu bot Discord (obtenha em https://discord.com/developers/applications)
# Substitua "SEU_TOKEN_AQUI" pelo token real do seu bot
DISCORD_TOKEN=SEU_TOKEN_AQUI

# IDs dos canais do Discord
DISCORD_GM_CHANNEL_ID=1234567890123456789
DISCORD_NEW_MEMBER_CHANNEL_ID=1378199753484926976
DISCORD_ANNOUNCEMENT_CHANNEL_ID=1333169997228281978

# URI do MongoDB
MONGODB_URI=mongodb://localhost:27017/
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Arquivo .env criado!")
    
    print("\n📋 Para obter seu token do Discord:")
    print("1. Acesse: https://discord.com/developers/applications")
    print("2. Selecione sua aplicação (bot)")
    print("3. Vá para a seção 'Bot' no menu lateral")
    print("4. Clique em 'Reset Token' para gerar um novo token")
    print("5. Copie o token gerado")
    
    print("\n🔑 Cole seu token aqui (ou pressione Enter para pular):")
    token = input("Token: ").strip()
    
    if token and token != "SEU_TOKEN_AQUI":
        # Atualizar o arquivo .env
        try:
            with open('.env', 'r') as f:
                lines = f.readlines()
            
            with open('.env', 'w') as f:
                for line in lines:
                    if line.startswith('DISCORD_TOKEN='):
                        f.write(f'DISCORD_TOKEN={token}\n')
                    else:
                        f.write(line)
            
            print("✅ Token atualizado com sucesso!")
            print("🔄 Agora você pode executar: python3 main.py")
            
        except Exception as e:
            print(f"❌ Erro ao atualizar token: {e}")
    else:
        print("⚠️ Token não foi atualizado.")
        print("📝 Edite manualmente o arquivo .env e substitua 'SEU_TOKEN_AQUI' pelo seu token real")

if __name__ == "__main__":
    setup_discord_token() 