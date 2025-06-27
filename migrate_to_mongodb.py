#!/usr/bin/env python3
"""
Script para migrar dados do arquivo saldos.json para MongoDB
Execute este script uma vez para migrar os dados existentes
"""

import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Configuração MongoDB
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGODB_URI)
db = client.bl4clabot
saldos_collection = db.saldos

def migrar_dados():
    """Migra dados do arquivo saldos.json para MongoDB"""
    
    # Verificar se existe o arquivo saldos.json
    if not os.path.exists("saldos.json"):
        print("❌ Arquivo saldos.json não encontrado!")
        return
    
    try:
        # Carregar dados do JSON
        with open("saldos.json", 'r') as f:
            dados_json = json.load(f)
        
        if not dados_json:
            print("ℹ️ Arquivo saldos.json está vazio. Nada para migrar.")
            return
        
        print(f"📊 Encontrados {len(dados_json)} usuários para migrar...")
        
        # Migrar cada usuário
        for user_id, saldo in dados_json.items():
            saldos_collection.update_one(
                {'user_id': user_id},
                {'$set': {'saldo': saldo}},
                upsert=True
            )
            print(f"✅ Migrado: {user_id} -> {saldo} VALs")
        
        print(f"🎉 Migração concluída! {len(dados_json)} usuários migrados para MongoDB.")
        
        # Verificar se a migração foi bem-sucedida
        total_mongodb = saldos_collection.count_documents({})
        print(f"📈 Total de usuários no MongoDB: {total_mongodb}")
        
    except Exception as e:
        print(f"❌ Erro durante a migração: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando migração para MongoDB...")
    migrar_dados() 