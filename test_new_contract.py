#!/usr/bin/env python3
"""
Script de teste para verificar se o novo contrato está funcionando corretamente
"""
from new_contract_utils import gerar_ranking_holders
import json

def test_new_contract():
    """Testa a funcionalidade do novo contrato."""
    print("🧪 Testando novo contrato KT1JhZBNxoMB3QzcdJfopmq3R5R6jPiwC1nw")
    print("=" * 60)
    
    try:
        # Gerar ranking
        ranking, total_holders, total_nfts = gerar_ranking_holders()
        
        print(f"✅ Ranking gerado com sucesso!")
        print(f"📊 Total de holders únicos: {total_holders}")
        print(f"📊 Total de NFTs: {total_nfts}")
        print()
        
        # Mostrar top 10
        print("🏆 Top 10 Holders:")
        print("-" * 40)
        for i, (address, alias, balance, tokens) in enumerate(ranking[:10], 1):
            name = f"{alias} ({address})" if alias else address
            print(f"{i:2d}. {name} - {balance} NFTs")
            
            # Mostrar detalhes dos tokens se houver mais de 1
            if len(tokens) > 1:
                for token in tokens:
                    print(f"     └─ {token['name']} (ID: {token['token_id']})")
        
        print()
        print("✅ Teste concluído com sucesso!")
        
        # Salvar resultado em arquivo
        with open('test_result.json', 'w', encoding='utf-8') as f:
            json.dump({
                'status': 'success',
                'total_holders': total_holders,
                'total_nfts': total_nfts,
                'top_10': [
                    {
                        'position': i,
                        'address': address,
                        'alias': alias,
                        'balance': balance,
                        'tokens': tokens
                    }
                    for i, (address, alias, balance, tokens) in enumerate(ranking[:10], 1)
                ]
            }, f, indent=2, ensure_ascii=False)
        
        print("💾 Resultado salvo em test_result.json")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        return False
    
    return True

if __name__ == '__main__':
    test_new_contract() 