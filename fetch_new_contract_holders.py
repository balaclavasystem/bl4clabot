#!/usr/bin/env python3
"""
Busca holders do novo contrato KT1JhZBNxoMB3QzcdJfopmq3R5R6jPiwC1nw via TzKT API
Mostra ranking por endereço e alias (se disponível), agrupando e somando corretamente.
"""
import requests
from collections import defaultdict
import json
from typing import Dict, List, Tuple, Optional, Any

NEW_CONTRACT = 'KT1JhZBNxoMB3QzcdJfopmq3R5R6jPiwC1nw'
TZKT_API = 'https://api.tzkt.io/v1'


def buscar_holders() -> List[Dict[str, Any]]:
    """Busca todos os holders do novo contrato."""
    url = f'{TZKT_API}/tokens/balances?token.contract={NEW_CONTRACT}&balance.ne=0&limit=1000'
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def buscar_alias(endereco: str) -> Optional[str]:
    """Busca o alias de um endereço."""
    url = f'{TZKT_API}/accounts/{endereco}'
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        if 'alias' in data and data['alias']:
            return data['alias']
    except:
        pass
    return None


def buscar_metadata_token(token_id: str) -> Dict[str, Any]:
    """Busca a metadata de um token específico."""
    url = f'{TZKT_API}/tokens?contract={NEW_CONTRACT}&tokenId={token_id}&limit=1'
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        if data and len(data) > 0:
            return data[0].get('metadata', {})
    except:
        pass
    return {}


def main():
    print(f"🔍 Buscando holders do novo contrato: {NEW_CONTRACT}")
    
    holders = buscar_holders()
    holders_dict: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
        'alias': None, 
        'balance': 0, 
        'tokens': []
    })
    
    for h in holders:
        address = h['account']['address']
        balance = int(h['balance'] or 0)
        token_id = h['token']['tokenId']
        
        # Buscar alias se ainda não foi buscado
        if holders_dict[address]['alias'] is None:
            holders_dict[address]['alias'] = buscar_alias(address)
        
        # Adicionar ao balance total
        current_balance = holders_dict[address]['balance']
        holders_dict[address]['balance'] = current_balance + balance
        
        # Adicionar token à lista
        token_metadata = buscar_metadata_token(token_id)
        if token_metadata:
            tokens_list = holders_dict[address]['tokens']
            tokens_list.append({
                'token_id': token_id,
                'name': token_metadata.get('name', f'Token #{token_id}'),
                'balance': balance
            })
    
    # Gerar ranking
    ranking: List[Tuple[str, Optional[str], int, List[Dict[str, Any]]]] = [
        (address, data['alias'], data['balance'], data['tokens']) 
        for address, data in holders_dict.items()
    ]
    ranking = [r for r in ranking if r[2] > 0]
    ranking.sort(key=lambda x: x[2], reverse=True)
    
    print('\n🏆 Ranking On-chain do Novo Contrato (agrupado por endereço):\n')
    for i, (address, alias, balance, tokens) in enumerate(ranking, 1):
        name = f'{alias} ({address})' if alias else address
        print(f'{i}. {name} - {balance} NFTs')
        
        # Mostrar detalhes dos tokens se houver mais de 1
        if len(tokens) > 1:
            for token in tokens:
                print(f'   └─ {token["name"]} (ID: {token["token_id"]})')
    
    total_holders = len(ranking)
    total_nfts = sum(x[2] for x in ranking)
    
    print(f'\n📊 Estatísticas:')
    print(f'Total de holders únicos: {total_holders}')
    print(f'Total de NFTs: {total_nfts}')
    
    # Exportar para CSV
    with open('new_contract_holders.csv', 'w', encoding='utf-8') as f:
        f.write('Posição,Endereço,Alias,Quantidade Total,Tokens\n')
        for i, (address, alias, balance, tokens) in enumerate(ranking, 1):
            token_names = '; '.join([f'{t["name"]}(ID:{t["token_id"]})' for t in tokens])
            f.write(f'{i},{address},{alias or ""},{balance},"{token_names}"\n')
    
    print('\n✅ Exportado para new_contract_holders.csv')
    
    # Salvar dados completos em JSON
    with open('new_contract_holders.json', 'w', encoding='utf-8') as f:
        json.dump({
            'contract': NEW_CONTRACT,
            'total_holders': total_holders,
            'total_nfts': total_nfts,
            'ranking': [
                {
                    'position': i,
                    'address': address,
                    'alias': alias,
                    'total_balance': balance,
                    'tokens': tokens
                }
                for i, (address, alias, balance, tokens) in enumerate(ranking, 1)
            ]
        }, f, indent=2, ensure_ascii=False)
    
    print('✅ Exportado para new_contract_holders.json')


if __name__ == '__main__':
    main() 