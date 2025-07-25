# Prompt para Criação de Script de Análise de Holders NFT

## Objetivo
Criar um script Python que analise holders de um contrato NFT na blockchain Tezos, gerando um ranking detalhado dos maiores holders.

## Requisitos Técnicos

### Dependências
```python
import requests
from collections import defaultdict
```

### Configurações
- **API:** TzKT (https://api.tzkt.io/v1)
- **Endpoint:** `/tokens/balances`
- **Parâmetros:** `token.contract={CONTRACT_ADDRESS}&balance.ne=0&limit=1000`

## Funcionalidades Obrigatórias

### 1. Busca de Dados
- Fazer requisição GET para a API TzKT
- Buscar todos os holders com balance > 0
- Agrupar por endereço (alguns endereços podem aparecer múltiplas vezes)

### 2. Processamento dos Dados
- Somar balances por endereço
- Filtrar apenas holders com balance > 0
- Calcular estatísticas gerais:
  - Total de holders únicos
  - Total de NFTs
  - Média de NFTs por holder

### 3. Análise por Grupos
- Agrupar holders por quantidade de NFTs
- Ordenar grupos do maior para o menor
- Mostrar quantos holders existem em cada grupo

### 4. Ranking Top 10
- Ordenar holders por quantidade de NFTs (decrescente)
- Mostrar endereços completos para os top 3
- Mostrar endereços abreviados para os demais (formato: `tz1XXXXXX...XXXXXX`)

### 5. Distribuição Estatística
- Calcular percentual de holders por grupo
- Calcular percentual de NFTs por grupo
- Criar faixas de distribuição (1 NFT, 2-5 NFTs, 6-10 NFTs, 11-20 NFTs, 21+ NFTs)

## Estrutura de Saída

### Estatísticas Gerais
```
📊 ESTATÍSTICAS GERAIS:
   Total de holders únicos: X
   Total de NFTs: X
   Média de NFTs por holder: X.XX
```

### Ranking por Quantidade
```
🏆 RANKING POR QUANTIDADE DE NFTs:
============================================================

📦 X NFTs (Y holder(s)):
   1. tz1XXXXXX...XXXXXX
   2. tz1XXXXXX...XXXXXX
   ... e mais Z holders
```

### Distribuição
```
📈 DISTRIBUIÇÃO:
============================================================
   X NFT(s):   Y holders (  Z.Z%) |   W NFTs (  V.V%)
```

### Top 10
```
🥇 TOP 10 HOLDERS:
============================================================
  🥇 tz1Tt1jmXYc7gGmpeBezqAdeojxJyphCYAL7 - 20 NFTs
  🥈 tz1LUv777uAZgT1QpvmEkpxxfKsh9h6ZgRTX - 15 NFTs
  🥉 tz1hYQYZrfcnbEQK3LqGxDwcYDc8pyFmuVco - 11 NFTs
  #4 tz1XXXXXX...XXXXXX - 7 NFTs
  ...
```

### Distribuição por Faixas
```
📊 DISTRIBUIÇÃO POR FAIXAS:
============================================================
  1 NFT: X holders (Y.Z%)
  2-5 NFTs: X holders (Y.Z%)
  6-10 NFTs: X holders (Y.Z%)
  11-20 NFTs: X holders (Y.Z%)
  21+ NFTs: X holders (Y.Z%)
```

## Tratamento de Erros
- Usar try/except para capturar erros de requisição
- Timeout de 30 segundos na requisição
- Verificar se a resposta tem status 200
- Retornar None em caso de erro

## Formatação
- Usar emojis para melhor visualização
- Separadores com "=" para organizar seções
- Formatação consistente de números e percentuais
- Endereços abreviados no formato padrão

## Exemplo de Uso
```python
if __name__ == "__main__":
    resultado = analise_rapida_holders()
    if resultado:
        print(f"\n✅ Análise concluída!")
    else:
        print(f"\n❌ Falha na análise")
```

## Variáveis de Configuração
```python
NEW_CONTRACT = 'KT1JhZBNxoMB3QzcdJfopmq3R5R6jPiwC1nw'  # Endereço do contrato
TZKT_API = 'https://api.tzkt.io/v1'  # URL da API
```

## Observações Importantes
- O script deve ser robusto e lidar com diferentes cenários de dados
- A formatação deve ser consistente e legível
- Os endereços completos devem ser mostrados apenas para os top 3
- O script deve funcionar com qualquer contrato NFT válido na Tezos 