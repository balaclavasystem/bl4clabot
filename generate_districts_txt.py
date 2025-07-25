#!/usr/bin/env python3
"""
Script para gerar arquivo TXT com Districts e NFTs em cada District
"""
import json
from new_contract_utils import buscar_todos_tokens, buscar_alias
from datetime import datetime


def gerar_arquivo_districts():
    """Gera arquivo TXT com Districts e NFTs em cada District."""
    print("🔍 Analisando NFTs e Districts...")
    
    # Buscar todos os tokens com suas metadatas
    tokens = buscar_todos_tokens()
    
    if not tokens:
        print("❌ Nenhum token encontrado!")
        return
    
    # Agrupar NFTs por District
    districts_data = {}
    total_nfts = len(tokens)
    
    for token in tokens:
        token_id = token.get('tokenId', 'Unknown')
        metadata = token.get('metadata', {})
        name = metadata.get('name', f'Token #{token_id}')
        
        # Buscar o trait District (primeiro trait)
        district_name = "Sem District"
        attributes = metadata.get('attributes', [])
        
        if isinstance(attributes, list) and len(attributes) > 0:
            first_attr = attributes[0]
            
            if isinstance(first_attr, dict):
                # Se tem trait_type, verificar se é district
                if 'trait_type' in first_attr and 'value' in first_attr:
                    trait_type = first_attr['trait_type'].lower()
                    if trait_type in ['district', 'distrito', 'area']:
                        district_name = str(first_attr['value'])
                elif 'name' in first_attr and 'value' in first_attr:
                    # Estrutura encontrada: {'name': 'District', 'value': 'Paper Street'}
                    if first_attr['name'].lower() in ['district', 'distrito', 'area']:
                        district_name = str(first_attr['value'])
                else:
                    # Se não tem trait_type, é o District (primeiro trait)
                    district_name = str(first_attr)
            else:
                # Se não é dict, é o District diretamente
                district_name = str(first_attr)
        
        # Adicionar ao District
        if district_name not in districts_data:
            districts_data[district_name] = {
                'count': 0,
                'percentage': 0,
                'nfts': []
            }
        
        districts_data[district_name]['count'] += 1
        districts_data[district_name]['nfts'].append({
            'token_id': token_id,
            'name': name
        })
    
    # Calcular percentuais
    for district_name, stats in districts_data.items():
        if total_nfts > 0:
            percentage = (stats['count'] / total_nfts) * 100
        else:
            percentage = 0
        stats['percentage'] = round(percentage, 2)
    
    # Ordenar Districts por número de NFTs
    sorted_districts = sorted(
        districts_data.items(), 
        key=lambda x: x[1]['count'], 
        reverse=True
    )
    
    # Gerar conteúdo do arquivo
    content = []
    content.append("=" * 60)
    content.append("🏛️  DISTRICTS - BALACLAVA SYSTEM")
    content.append("=" * 60)
    content.append(f"📅 Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    content.append(f"🌍 Total de Districts: {len(districts_data)}")
    content.append(f"🎨 Total de NFTs: {total_nfts}")
    content.append("")
    
    # Adicionar cada District
    for i, (district_name, stats) in enumerate(sorted_districts, 1):
        content.append(f"{'='*50}")
        content.append(f"🏛️  DISTRICT #{i}: {district_name.upper()}")
        content.append(f"{'='*50}")
        content.append(f"📊 Estatísticas:")
        content.append(f"   • NFTs no District: {stats['count']}")
        content.append(f"   • Percentual do total: {stats['percentage']}%")
        content.append("")
        
        if stats['nfts']:
            content.append("🎨 NFTs neste District:")
            content.append("-" * 30)
            
            # Ordenar NFTs por token_id
            sorted_nfts = sorted(stats['nfts'], key=lambda x: int(x['token_id']))
            
            for j, nft in enumerate(sorted_nfts, 1):
                content.append(f"{j:2d}. {nft['name']} (ID: {nft['token_id']})")
        else:
            content.append("🎨 NFTs: Nenhum NFT encontrado")
        
        content.append("")
    
    # Adicionar resumo final
    content.append("=" * 60)
    content.append("📋 RESUMO GERAL")
    content.append("=" * 60)
    
    for i, (district_name, stats) in enumerate(sorted_districts, 1):
        emoji = "🏛️"
        if stats['count'] >= 20:
            emoji = "🏛️🔥"
        elif stats['count'] >= 15:
            emoji = "🏛️⚡"
        elif stats['count'] >= 10:
            emoji = "🏛️💎"
        elif stats['count'] >= 5:
            emoji = "🏛️⭐"
        
        content.append(f"{i:2d}. {emoji} {district_name}: {stats['count']} NFTs ({stats['percentage']}%)")
    
    content.append("")
    content.append("=" * 60)
    content.append("✅ Arquivo gerado com sucesso!")
    content.append("=" * 60)
    
    # Salvar arquivo
    filename = f"districts_nfts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    
    print(f"✅ Arquivo gerado: {filename}")
    print(f"📊 Total de Districts: {len(districts_data)}")
    print(f"🎨 Total de NFTs: {total_nfts}")
    
    return filename


if __name__ == "__main__":
    try:
        filename = gerar_arquivo_districts()
        if filename:
            print(f"\n📁 Arquivo salvo como: {filename}")
    except Exception as e:
        print(f"❌ Erro ao gerar arquivo: {e}") 