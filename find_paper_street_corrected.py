#!/usr/bin/env python3
"""
Script corrigido para localizar o District "Paper Street" nos NFTs
"""
from new_contract_utils import buscar_todos_tokens
from datetime import datetime


def encontrar_paper_street_corrigido():
    """Localiza NFTs no District Paper Street (versão corrigida)."""
    print("🔍 Procurando por District 'Paper Street' (versão corrigida)...")
    
    # Buscar todos os tokens com suas metadatas
    tokens = buscar_todos_tokens()
    
    if not tokens:
        print("❌ Nenhum token encontrado!")
        return
    
    # Procurar por Paper Street
    paper_street_nfts = []
    total_nfts = len(tokens)
    districts_encontrados = set()
    
    for token in tokens:
        token_id = token.get('tokenId', 'Unknown')
        metadata = token.get('metadata', {})
        name = metadata.get('name', f'Token #{token_id}')
        
        # Buscar o trait District (primeiro trait sem trait_type)
        attributes = metadata.get('attributes', [])
        
        if isinstance(attributes, list) and len(attributes) > 0:
            # O primeiro trait é o District
            first_attr = attributes[0]
            
            if isinstance(first_attr, dict):
                # Se tem trait_type, verificar se é district
                if 'trait_type' in first_attr and 'value' in first_attr:
                    trait_type = first_attr['trait_type'].lower()
                    trait_value = str(first_attr['value'])
                    
                    if trait_type in ['district', 'distrito', 'area']:
                        districts_encontrados.add(trait_value)
                        
                        # Procurar por "paper street" (case insensitive)
                        if 'paper street' in trait_value.lower() or 'paperstreet' in trait_value.lower():
                            paper_street_nfts.append({
                                'token_id': token_id,
                                'name': name,
                                'district': trait_value
                            })
                else:
                    # Se não tem trait_type, é o District (primeiro trait)
                    district_value = str(first_attr)
                    districts_encontrados.add(district_value)
                    
                    # Procurar por "paper street" (case insensitive)
                    if 'paper street' in district_value.lower() or 'paperstreet' in district_value.lower():
                        paper_street_nfts.append({
                            'token_id': token_id,
                            'name': name,
                            'district': district_value
                        })
            else:
                # Se não é dict, é o District diretamente
                district_value = str(first_attr)
                districts_encontrados.add(district_value)
                
                # Procurar por "paper street" (case insensitive)
                if 'paper street' in district_value.lower() or 'paperstreet' in district_value.lower():
                    paper_street_nfts.append({
                        'token_id': token_id,
                        'name': name,
                        'district': district_value
                    })
    
    # Gerar relatório
    print(f"\n📊 RESULTADO DA BUSCA:")
    print(f"🎨 Total de NFTs analisados: {total_nfts}")
    print(f"🏛️  NFTs encontrados no District 'Paper Street': {len(paper_street_nfts)}")
    print(f"🌍 Districts únicos encontrados: {len(districts_encontrados)}")
    
    if paper_street_nfts:
        print(f"\n✅ NFTs no District 'Paper Street':")
        print("=" * 50)
        
        # Ordenar por token_id
        sorted_nfts = sorted(paper_street_nfts, key=lambda x: int(x['token_id']))
        
        for i, nft in enumerate(sorted_nfts, 1):
            print(f"{i:2d}. {nft['name']} (ID: {nft['token_id']})")
            print(f"    District: {nft['district']}")
            print()
        
        # Salvar em arquivo
        filename = f"paper_street_nfts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("DISTRICT PAPER STREET - BALACLAVA SYSTEM\n")
            f.write("=" * 50 + "\n")
            f.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Total de NFTs analisados: {total_nfts}\n")
            f.write(f"NFTs encontrados: {len(paper_street_nfts)}\n\n")
            
            for i, nft in enumerate(sorted_nfts, 1):
                f.write(f"{i:2d}. {nft['name']} (ID: {nft['token_id']})\n")
                f.write(f"    District: {nft['district']}\n\n")
        
        print(f"📁 Arquivo salvo: {filename}")
        
    else:
        print("\n❌ Nenhum NFT encontrado no District 'Paper Street'")
    
    # Mostrar todos os Districts encontrados
    if districts_encontrados:
        print(f"\n🏛️  Todos os Districts encontrados no contrato:")
        for district in sorted(districts_encontrados):
            print(f"   • {district}")
    
    return paper_street_nfts


if __name__ == "__main__":
    try:
        nfts = encontrar_paper_street_corrigido()
        if nfts:
            print(f"\n✅ Encontrados {len(nfts)} NFTs no District 'Paper Street'")
        else:
            print(f"\n❌ Nenhum NFT encontrado no District 'Paper Street'")
    except Exception as e:
        print(f"❌ Erro ao buscar: {e}") 