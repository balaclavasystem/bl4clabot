#!/usr/bin/env python3
"""
Script para gerar arquivo TXT simples com Districts e NFTs
"""
from new_contract_utils import buscar_todos_tokens
from datetime import datetime


def gerar_arquivo_simples():
    """Gera arquivo TXT simples com Districts e NFTs."""
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
        
        # Buscar o trait District
        district_name = "Sem District"
        attributes = metadata.get('attributes', [])
        
        if isinstance(attributes, list):
            for attr in attributes:
                if isinstance(attr, dict) and 'trait_type' in attr and 'value' in attr:
                    if attr['trait_type'].lower() in ['district', 'distrito', 'area']:
                        district_name = str(attr['value'])
                        break
        
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
    
    # Gerar conteúdo simples
    content = []
    content.append("DISTRICTS - BALACLAVA SYSTEM")
    content.append("=" * 40)
    content.append(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    content.append(f"Total de Districts: {len(districts_data)}")
    content.append(f"Total de NFTs: {total_nfts}")
    content.append("")
    
    # Adicionar cada District
    for i, (district_name, stats) in enumerate(sorted_districts, 1):
        content.append(f"DISTRICT #{i}: {district_name}")
        content.append(f"  NFTs: {stats['count']} | %: {stats['percentage']}%")
        content.append("")
        
        if stats['nfts']:
            content.append("  NFTs neste District:")
            # Ordenar NFTs por token_id
            sorted_nfts = sorted(stats['nfts'], key=lambda x: int(x['token_id']))
            
            for nft in sorted_nfts:
                content.append(f"    • {nft['name']} (ID: {nft['token_id']})")
        else:
            content.append("  NFTs: Nenhum")
        
        content.append("")
        content.append("-" * 40)
        content.append("")
    
    # Salvar arquivo
    filename = f"districts_simples_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    
    print(f"✅ Arquivo simples gerado: {filename}")
    return filename


if __name__ == "__main__":
    try:
        filename = gerar_arquivo_simples()
        if filename:
            print(f"\n📁 Arquivo salvo como: {filename}")
    except Exception as e:
        print(f"❌ Erro ao gerar arquivo: {e}") 