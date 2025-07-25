#!/usr/bin/env python3
"""
Script para localizar o District "Paper Street" nos NFTs
"""
from new_contract_utils import buscar_todos_tokens
from datetime import datetime


def encontrar_paper_street():
    """Localiza NFTs no District Paper Street."""
    print("🔍 Procurando por District 'Paper Street'...")
    
    # Buscar todos os tokens com suas metadatas
    tokens = buscar_todos_tokens()
    
    if not tokens:
        print("❌ Nenhum token encontrado!")
        return
    
    # Procurar por Paper Street
    paper_street_nfts = []
    total_nfts = len(tokens)
    
    for token in tokens:
        token_id = token.get('tokenId', 'Unknown')
        metadata = token.get('metadata', {})
        name = metadata.get('name', f'Token #{token_id}')
        
        # Buscar o trait District
        attributes = metadata.get('attributes', [])
        
        if isinstance(attributes, list):
            for attr in attributes:
                if isinstance(attr, dict) and 'trait_type' in attr and 'value' in attr:
                    if attr['trait_type'].lower() in ['district', 'distrito', 'area']:
                        district_value = str(attr['value']).lower()
                        
                        # Procurar por "paper street" (case insensitive)
                        if 'paper street' in district_value or 'paperstreet' in district_value:
                            paper_street_nfts.append({
                                'token_id': token_id,
                                'name': name,
                                'district': attr['value']
                            })
                            break
    
    # Gerar relatório
    print(f"\n📊 RESULTADO DA BUSCA:")
    print(f"🎨 Total de NFTs analisados: {total_nfts}")
    print(f"🏛️  NFTs encontrados no District 'Paper Street': {len(paper_street_nfts)}")
    
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
        print("💡 Verificando se há outros Districts similares...")
        
        # Listar todos os Districts encontrados
        districts_found = set()
        for token in tokens:
            metadata = token.get('metadata', {})
            attributes = metadata.get('attributes', [])
            
            if isinstance(attributes, list):
                for attr in attributes:
                    if isinstance(attr, dict) and 'trait_type' in attr and 'value' in attr:
                        if attr['trait_type'].lower() in ['district', 'distrito', 'area']:
                            districts_found.add(str(attr['value']))
        
        if districts_found:
            print(f"\n🏛️  Districts encontrados no contrato:")
            for district in sorted(districts_found):
                print(f"   • {district}")
        else:
            print("\n🏛️  Nenhum District encontrado nos metadados dos NFTs")
    
    return paper_street_nfts


if __name__ == "__main__":
    try:
        nfts = encontrar_paper_street()
        if nfts:
            print(f"\n✅ Encontrados {len(nfts)} NFTs no District 'Paper Street'")
        else:
            print(f"\n❌ Nenhum NFT encontrado no District 'Paper Street'")
    except Exception as e:
        print(f"❌ Erro ao buscar: {e}") 