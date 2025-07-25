#!/usr/bin/env python3
"""
Script para analisar o ranking de holders do contrato KT1JhZBNxoMB3QzcdJfopmq3R5R6jPiwC1nw
Agrupa holders por quantidade de NFTs
"""

import json
from collections import defaultdict
from new_contract_utils import gerar_ranking_holders, analisar_districts
import requests

def analisar_ranking_por_quantidade():
    """Analisa o ranking de holders agrupados por quantidade de NFTs"""
    
    print("🔍 Analisando holders do contrato KT1JhZBNxoMB3QzcdJfopmq3R5R6jPiwC1nw...")
    
    try:
        # Gerar ranking completo
        ranking, total_holders, total_nfts = gerar_ranking_holders()
        
        print(f"\n📊 ESTATÍSTICAS GERAIS:")
        print(f"   Total de holders únicos: {total_holders}")
        print(f"   Total de NFTs: {total_nfts}")
        print(f"   Média de NFTs por holder: {total_nfts/total_holders:.2f}")
        
        # Agrupar por quantidade
        grupos_quantidade = defaultdict(list)
        for address, alias, balance, tokens in ranking:
            grupos_quantidade[balance].append({
                'address': address,
                'alias': alias,
                'tokens': tokens
            })
        
        # Ordenar grupos por quantidade (decrescente)
        grupos_ordenados = sorted(grupos_quantidade.items(), reverse=True)
        
        print(f"\n🏆 RANKING POR QUANTIDADE DE NFTs:")
        print("=" * 80)
        
        for quantidade, holders in grupos_ordenados:
            print(f"\n📦 {quantidade} NFT{'s' if quantidade > 1 else ''} ({len(holders)} holder{'s' if len(holders) > 1 else ''}):")
            print("-" * 50)
            
            for i, holder in enumerate(holders, 1):
                alias = holder['alias'] if holder['alias'] else "Sem alias"
                address_short = f"{holder['address'][:8]}...{holder['address'][-6:]}"
                
                print(f"  {i:2d}. {alias} ({address_short})")
                
                # Mostrar detalhes dos tokens se houver mais de 1
                if len(holder['tokens']) > 1:
                    for token in holder['tokens']:
                        print(f"      └─ {token['name']} (ID: {token['token_id']})")
        
        # Análise de distribuição
        print(f"\n📈 DISTRIBUIÇÃO:")
        print("=" * 80)
        
        for quantidade, holders in grupos_ordenados:
            percentual = (len(holders) / total_holders) * 100
            nfts_grupo = quantidade * len(holders)
            percentual_nfts = (nfts_grupo / total_nfts) * 100
            
            print(f"  {quantidade:2d} NFT{'s' if quantidade > 1 else '':>2}: {len(holders):3d} holders ({percentual:5.1f}%) | {nfts_grupo:3d} NFTs ({percentual_nfts:5.1f}%)")
        
        # Top 10 holders
        print(f"\n🥇 TOP 10 HOLDERS:")
        print("=" * 80)
        
        for i, (address, alias, balance, tokens) in enumerate(ranking[:10], 1):
            alias = alias if alias else "Sem alias"
            address_short = f"{address[:8]}...{address[-6:]}"
            
            medalha = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"#{i}"
            print(f"  {medalha} {alias} ({address_short}) - {balance} NFT{'s' if balance > 1 else ''}")
        
        # Análise de Districts
        print(f"\n🗺️  ANÁLISE DE DISTRICTS:")
        print("=" * 80)
        
        districts_data = analisar_districts()
        districts_ordenados = sorted(districts_data.items(), key=lambda x: x[1]['count'], reverse=True)
        
        for district_name, stats in districts_ordenados:
            print(f"  {district_name}: {stats['count']} NFTs ({stats['percentage']:.1f}%) | {stats['unique_members']} membros únicos")
        
        # Salvar dados em JSON
        dados_completos = {
            'estatisticas_gerais': {
                'total_holders': total_holders,
                'total_nfts': total_nfts,
                'media_nfts_por_holder': round(total_nfts/total_holders, 2)
            },
            'ranking_completo': [
                {
                    'posicao': i+1,
                    'address': address,
                    'alias': alias,
                    'balance': balance,
                    'tokens': tokens
                }
                for i, (address, alias, balance, tokens) in enumerate(ranking)
            ],
            'grupos_por_quantidade': {
                str(quantidade): {
                    'quantidade_holders': len(holders),
                    'total_nfts_grupo': quantidade * len(holders),
                    'holders': [
                        {
                            'address': h['address'],
                            'alias': h['alias'],
                            'tokens': h['tokens']
                        }
                        for h in holders
                    ]
                }
                for quantidade, holders in grupos_ordenados
            },
            'districts': districts_data
        }
        
        with open('ranking_holders_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(dados_completos, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Dados salvos em 'ranking_holders_analysis.json'")
        
        return dados_completos
        
    except Exception as e:
        print(f"❌ Erro ao analisar holders: {e}")
        return None

def gerar_relatorio_resumido():
    """Gera um relatório resumido do ranking"""
    
    try:
        ranking, total_holders, total_nfts = gerar_ranking_holders()
        
        print(f"\n📋 RELATÓRIO RESUMIDO:")
        print("=" * 50)
        print(f"Total de holders: {total_holders}")
        print(f"Total de NFTs: {total_nfts}")
        print(f"Média: {total_nfts/total_holders:.2f} NFTs/holder")
        
        # Distribuição por faixas
        faixas = {
            '1 NFT': 0,
            '2-5 NFTs': 0,
            '6-10 NFTs': 0,
            '11-20 NFTs': 0,
            '21+ NFTs': 0
        }
        
        for _, _, balance, _ in ranking:
            if balance == 1:
                faixas['1 NFT'] += 1
            elif 2 <= balance <= 5:
                faixas['2-5 NFTs'] += 1
            elif 6 <= balance <= 10:
                faixas['6-10 NFTs'] += 1
            elif 11 <= balance <= 20:
                faixas['11-20 NFTs'] += 1
            else:
                faixas['21+ NFTs'] += 1
        
        print(f"\n📊 Distribuição por faixas:")
        for faixa, quantidade in faixas.items():
            percentual = (quantidade / total_holders) * 100
            print(f"  {faixa}: {quantidade} holders ({percentual:.1f}%)")
        
        return faixas
        
    except Exception as e:
        print(f"❌ Erro ao gerar relatório: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Iniciando análise de holders...")
    
    # Análise completa
    dados = analisar_ranking_por_quantidade()
    
    if dados:
        print(f"\n✅ Análise concluída com sucesso!")
        
        # Relatório resumido
        gerar_relatorio_resumido()
    else:
        print(f"\n❌ Falha na análise") 