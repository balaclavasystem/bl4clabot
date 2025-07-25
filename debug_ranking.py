#!/usr/bin/env python3
"""
Script de debug para testar apenas a função de ranking
"""
from new_contract_utils import gerar_ranking_holders

def test_ranking():
    print("🧪 Testando função de ranking...")
    
    try:
        print("📊 Gerando ranking...")
        ranking, total_holders, total_nfts = gerar_ranking_holders()
        
        print(f"✅ Ranking gerado com sucesso!")
        print(f"📊 Total de holders: {total_holders}")
        print(f"📊 Total de NFTs: {total_nfts}")
        
        if ranking:
            print("\n🏆 Top 5 Holders:")
            for i, (address, alias, balance, tokens) in enumerate(ranking[:5], 1):
                name = f"{alias} ({address})" if alias else address
                print(f"{i}. {name} - {balance} NFTs")
        else:
            print("❌ Nenhum holder encontrado")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_ranking() 