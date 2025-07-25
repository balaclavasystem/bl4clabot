#!/usr/bin/env python3
"""
Utilitários para buscar holders do novo contrato KT1JhZBNxoMB3QzcdJfopmq3R5R6jPiwC1nw
"""
import requests
from collections import defaultdict
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


def buscar_todos_tokens() -> List[Dict[str, Any]]:
    """Busca todos os tokens do contrato com suas metadatas."""
    url = f'{TZKT_API}/tokens?contract={NEW_CONTRACT}&limit=1000'
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json()
    except:
        return []


def analisar_traits() -> Dict[str, Dict[str, Dict[str, Any]]]:
    """
    Analisa todos os traits dos NFTs e retorna estatísticas.
    
    Returns:
        Dict com estrutura: {trait_category: {trait_value: {count: X, percentage: Y}}}
    """
    tokens = buscar_todos_tokens()
    total_tokens = len(tokens)
    
    if total_tokens == 0:
        return {}
    
    traits_stats = defaultdict(lambda: defaultdict(lambda: {'count': 0, 'percentage': 0}))
    
    for token in tokens:
        metadata = token.get('metadata', {})
        attributes = metadata.get('attributes', [])
        
        if isinstance(attributes, list):
            for attr in attributes:
                if isinstance(attr, dict) and 'trait_type' in attr and 'value' in attr:
                    trait_type = attr['trait_type']
                    trait_value = str(attr['value'])
                    
                    traits_stats[trait_type][trait_value]['count'] += 1
    
    # Calcular percentuais
    for trait_type in traits_stats:
        for trait_value in traits_stats[trait_type]:
            count = traits_stats[trait_type][trait_value]['count']
            percentage = (count / total_tokens) * 100
            traits_stats[trait_type][trait_value]['percentage'] = round(percentage, 2)
    
    return dict(traits_stats)


def analisar_districts() -> Dict[str, Dict[str, Any]]:
    """
    Analisa os Districts dos NFTs e conta membros por District.
    
    Returns:
        Dict com estrutura: {district_name: {count: X, percentage: Y, members: [addresses]}}
    """
    holders = buscar_holders()
    districts_stats = defaultdict(lambda: {'count': 0, 'percentage': 0, 'members': set()})
    total_nfts = 0
    
    for holder in holders:
        address = holder['account']['address']
        balance = int(holder['balance'] or 0)
        token_id = holder['token']['tokenId']
        
        if balance > 0:
            total_nfts += balance
            
            # Buscar metadata do token para verificar o District
            metadata = buscar_metadata_token(token_id)
            attributes = metadata.get('attributes', [])
            
            district_name = "Sem District"
            if isinstance(attributes, list):
                for attr in attributes:
                    if isinstance(attr, dict) and 'trait_type' in attr and 'value' in attr:
                        if attr['trait_type'].lower() in ['district', 'distrito', 'area']:
                            district_name = str(attr['value'])
                            break
            
            districts_stats[district_name]['count'] += balance
            districts_stats[district_name]['members'].add(address)
    
    # Calcular percentuais e converter sets para listas
    result = {}
    for district_name, stats in districts_stats.items():
        if total_nfts > 0:
            percentage = (stats['count'] / total_nfts) * 100
        else:
            percentage = 0
            
        result[district_name] = {
            'count': stats['count'],
            'percentage': round(percentage, 2),
            'members': list(stats['members']),
            'unique_members': len(stats['members'])
        }
    
    return result


def gerar_ranking_holders() -> Tuple[List[Tuple[str, Optional[str], int, List[Dict[str, Any]]]], int, int]:
    """
    Gera o ranking completo dos holders do novo contrato.
    
    Returns:
        Tuple contendo:
        - Lista de tuplas (address, alias, balance, tokens)
        - Total de holders únicos
        - Total de NFTs
    """
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
            if isinstance(tokens_list, list):
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
    
    total_holders = len(ranking)
    total_nfts = sum(x[2] for x in ranking)
    
    return ranking, total_holders, total_nfts 