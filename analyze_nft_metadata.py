#!/usr/bin/env python3
"""
Script para analisar detalhadamente os metadados dos NFTs
"""
from new_contract_utils import buscar_todos_tokens
import json


def analisar_metadados():
    """Analisa detalhadamente os metadados dos NFTs."""
    print("🔍 Analisando metadados dos NFTs...")
    
    # Buscar todos os tokens
    tokens = buscar_todos_tokens()
    
    if not tokens:
        print("❌ Nenhum token encontrado!")
        return
    
    print(f"📊 Total de NFTs encontrados: {len(tokens)}")
    print("\n🔍 Analisando os primeiros 5 NFTs em detalhes:")
    print("=" * 60)
    
    # Analisar os primeiros 5 NFTs em detalhes
    for i, token in enumerate(tokens[:5], 1):
        token_id = token.get('tokenId', 'Unknown')
        metadata = token.get('metadata', {})
        name = metadata.get('name', f'Token #{token_id}')
        
        print(f"\n🎨 NFT #{i}: {name} (ID: {token_id})")
        print("-" * 40)
        
        # Mostrar todos os campos do metadata
        print("📋 Campos do metadata:")
        for key, value in metadata.items():
            if key == 'attributes':
                print(f"   • {key}: {len(value) if isinstance(value, list) else value} items")
            else:
                print(f"   • {key}: {value}")
        
        # Analisar attributes em detalhes
        attributes = metadata.get('attributes', [])
        if attributes:
            print(f"\n🏷️  Traits/Attributes ({len(attributes)} encontrados):")
            for j, attr in enumerate(attributes, 1):
                if isinstance(attr, dict):
                    trait_type = attr.get('trait_type', 'Unknown')
                    trait_value = attr.get('value', 'Unknown')
                    print(f"   {j:2d}. {trait_type}: {trait_value}")
                else:
                    print(f"   {j:2d}. {attr}")
        else:
            print("\n🏷️  Traits/Attributes: Nenhum encontrado")
        
        print()
    
    # Verificar se há algum NFT com District
    print("🔍 Verificando todos os NFTs por Districts...")
    districts_encontrados = set()
    nfts_com_district = 0
    
    for token in tokens:
        metadata = token.get('metadata', {})
        attributes = metadata.get('attributes', [])
        
        if isinstance(attributes, list):
            for attr in attributes:
                if isinstance(attr, dict) and 'trait_type' in attr and 'value' in attr:
                    trait_type = attr['trait_type'].lower()
                    trait_value = str(attr['value'])
                    
                    if trait_type in ['district', 'distrito', 'area']:
                        districts_encontrados.add(trait_value)
                        nfts_com_district += 1
                        break
    
    print(f"\n📊 RESULTADO DA ANÁLISE:")
    print(f"🎨 Total de NFTs: {len(tokens)}")
    print(f"🏛️  NFTs com District: {nfts_com_district}")
    print(f"🌍 Districts encontrados: {len(districts_encontrados)}")
    
    if districts_encontrados:
        print(f"\n🏛️  Districts encontrados:")
        for district in sorted(districts_encontrados):
            print(f"   • {district}")
    else:
        print(f"\n🏛️  Nenhum District encontrado")
    
    # Verificar todos os tipos de traits encontrados
    print(f"\n🔍 Verificando todos os tipos de traits...")
    trait_types = set()
    
    for token in tokens:
        metadata = token.get('metadata', {})
        attributes = metadata.get('attributes', [])
        
        if isinstance(attributes, list):
            for attr in attributes:
                if isinstance(attr, dict) and 'trait_type' in attr:
                    trait_types.add(attr['trait_type'])
    
    if trait_types:
        print(f"\n🏷️  Tipos de traits encontrados ({len(trait_types)}):")
        for trait_type in sorted(trait_types):
            print(f"   • {trait_type}")
    else:
        print(f"\n🏷️  Nenhum trait encontrado")


if __name__ == "__main__":
    try:
        analisar_metadados()
    except Exception as e:
        print(f"❌ Erro ao analisar: {e}") 