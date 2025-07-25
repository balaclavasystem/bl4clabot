#!/usr/bin/env python3
"""
Script para testar os comandos do bot
"""

import json
import os

def test_saldos_system():
    """Testa o sistema de saldos"""
    print("🧪 Testando sistema de saldos...")
    
    # Simular algumas operações
    saldos = {}
    
    # Adicionar VALs para alguns usuários
    saldos["123456789"] = 10
    saldos["987654321"] = 25
    saldos["555666777"] = 5
    
    # Salvar no arquivo
    with open("saldos.json", "w", encoding="utf-8") as f:
        json.dump(saldos, f, indent=2, ensure_ascii=False)
    
    print("✅ Saldos salvos no arquivo saldos.json")
    
    # Carregar e mostrar
    with open("saldos.json", "r", encoding="utf-8") as f:
        saldos_carregados = json.load(f)
    
    print("📊 Saldos carregados:")
    for user_id, saldo in saldos_carregados.items():
        print(f"  Usuário {user_id}: {saldo} VALs")
    
    # Testar ranking
    ranking = sorted(saldos_carregados.items(), key=lambda x: x[1], reverse=True)
    print("\n🏆 Ranking:")
    for i, (user_id, saldo) in enumerate(ranking, 1):
        medalha = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"#{i}"
        print(f"  {medalha} Usuário {user_id}: {saldo} VALs")

def test_new_contract_utils():
    """Testa as funções do novo contrato"""
    print("\n🧪 Testando funções do novo contrato...")
    
    try:
        from new_contract_utils import gerar_ranking_holders
        ranking = gerar_ranking_holders()
        
        if ranking:
            print(f"✅ Ranking gerado com {len(ranking)} holders")
            print("📊 Top 5 holders:")
            for i, holder in enumerate(ranking[:5], 1):
                print(f"  #{i} {holder['address'][:8]}...{holder['address'][-6:]}: {holder['balance']} NFTs")
        else:
            print("❌ Nenhum holder encontrado")
            
    except Exception as e:
        print(f"❌ Erro ao testar: {e}")

if __name__ == "__main__":
    print("🔧 Testando funcionalidades do bot...")
    print("=" * 50)
    
    test_saldos_system()
    test_new_contract_utils()
    
    print("\n" + "=" * 50)
    print("✅ Testes concluídos!")
    print("\n📋 Para usar o bot:")
    print("1. Execute: python3 main_no_mongodb.py")
    print("2. Teste os comandos no Discord:")
    print("   - /ping")
    print("   - /saldo")
    print("   - /posicao")
    print("   - /rankingholders")
    print("   - /talk (apenas admins)") 