#!/usr/bin/env python3
"""
Análise rápida de holders do contrato
"""

import requests
from collections import defaultdict

NEW_CONTRACT = 'KT1JhZBNxoMB3QzcdJfopmq3R5R6jPiwC1nw'
TZKT_API = 'https://api.tzkt.io/v1'

def analise_rapida_holders():
    """Análise rápida dos holders"""
    
    print("🔍 Analisando holders rapidamente...")
    
    try:
        # Buscar holders
        url = f'{TZKT_API}/tokens/balances?token.contract={NEW_CONTRACT}&balance.ne=0&limit=1000'
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        holders = resp.json()
        
        print(f"✅ {len(holders)} registros encontrados")
        
        # Agrupar por endereço
        holders_por_endereco = defaultdict(int)
        
        for holder in holders:
            address = holder['account']['address']
            balance = int(holder['balance'] or 0)
            holders_por_endereco[address] += balance
        
        # Filtrar apenas holders com balance > 0
        holders_filtrados = {addr: bal for addr, bal in holders_por_endereco.items() if bal > 0}
        
        # Estatísticas gerais
        total_holders = len(holders_filtrados)
        total_nfts = sum(holders_filtrados.values())
        
        print(f"\n📊 ESTATÍSTICAS GERAIS:")
        print(f"   Total de holders únicos: {total_holders}")
        print(f"   Total de NFTs: {total_nfts}")
        print(f"   Média de NFTs por holder: {total_nfts/total_holders:.2f}")
        
        # Agrupar por quantidade
        grupos_quantidade = defaultdict(list)
        for address, balance in holders_filtrados.items():
            grupos_quantidade[balance].append(address)
        
        # Ordenar grupos
        grupos_ordenados = sorted(grupos_quantidade.items(), reverse=True)
        
        print(f"\n🏆 RANKING POR QUANTIDADE DE NFTs:")
        print("=" * 60)
        
        for quantidade, addresses in grupos_ordenados:
            print(f"\n📦 {quantidade} NFT{'s' if quantidade > 1 else ''} ({len(addresses)} holder{'s' if len(addresses) > 1 else ''}):")
            
            # Mostrar apenas os primeiros 5 de cada grupo
            for i, address in enumerate(addresses[:5], 1):
                address_short = f"{address[:8]}...{address[-6:]}"
                print(f"  {i:2d}. {address_short}")
            
            if len(addresses) > 5:
                print(f"  ... e mais {len(addresses) - 5} holders")
        
        # Distribuição
        print(f"\n📈 DISTRIBUIÇÃO:")
        print("=" * 60)
        
        for quantidade, addresses in grupos_ordenados:
            percentual = (len(addresses) / total_holders) * 100
            nfts_grupo = quantidade * len(addresses)
            percentual_nfts = (nfts_grupo / total_nfts) * 100
            
            print(f"  {quantidade:2d} NFT{'s' if quantidade > 1 else '':>2}: {len(addresses):3d} holders ({percentual:5.1f}%) | {nfts_grupo:3d} NFTs ({percentual_nfts:5.1f}%)")
        
        # Top 10
        ranking = sorted(holders_filtrados.items(), key=lambda x: x[1], reverse=True)
        
        print(f"\n🥇 TOP 10 HOLDERS:")
        print("=" * 60)
        
        for i, (address, balance) in enumerate(ranking[:10], 1):
            if i <= 3:
                # Mostrar endereço completo para os top 3
                medalha = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"#{i}"
                print(f"  {medalha} {address} - {balance} NFT{'s' if balance > 1 else ''}")
            else:
                # Mostrar endereço abreviado para os demais
                address_short = f"{address[:8]}...{address[-6:]}"
                medalha = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"#{i}"
                print(f"  {medalha} {address_short} - {balance} NFT{'s' if balance > 1 else ''}")
        
        # Análise por faixas
        faixas = {
            '1 NFT': 0,
            '2-5 NFTs': 0,
            '6-10 NFTs': 0,
            '11-20 NFTs': 0,
            '21+ NFTs': 0
        }
        
        for _, balance in holders_filtrados.items():
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
        
        print(f"\n📊 DISTRIBUIÇÃO POR FAIXAS:")
        print("=" * 60)
        for faixa, quantidade in faixas.items():
            percentual = (quantidade / total_holders) * 100
            print(f"  {faixa}: {quantidade} holders ({percentual:.1f}%)")
        
        return {
            'total_holders': total_holders,
            'total_nfts': total_nfts,
            'grupos': dict(grupos_ordenados),
            'faixas': faixas,
            'top_10': ranking[:10]
        }
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

if __name__ == "__main__":
    resultado = analise_rapida_holders()
    if resultado:
        print(f"\n✅ Análise concluída!")
    else:
        print(f"\n❌ Falha na análise") 