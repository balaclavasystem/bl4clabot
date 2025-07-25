# 🤖 Bot Discord - Balaclava System

Bot Discord para gerenciar a comunidade Balaclava System, com sistema de moeda virtual (VALs) e ranking de holders do novo contrato NFT.

## 📋 Sobre o Projeto

Este bot foi desenvolvido para:
- Gerenciar sistema de moeda virtual (VALs) para a comunidade
- Criar ranking de holders do contrato NFT da Balaclava System
- Enviar mensagens GM automáticas
- Facilitar comunicação entre membros

## 🆕 Contrato NFT Atual

**Contrato**: `KT1JhZBNxoMB3QzcdJfopmq3R5R6jPiwC1nw`

### Características do Contrato
- **Padrão**: FA2 (Tezos NFT)
- **Tokens**: 85 NFTs únicos com metadata rica
- **Informações**: Nome, District, Age, Balaclava, Background, Member Since, Item

## 🚀 Funcionalidades

### Sistema de Moeda (VALs)
- **Comando**: `/saldo` - Verificar saldo de VALs
- **Comando**: `/posicao` - Ver ranking de VALs
- **Comando**: `/darvals` - Adicionar VALs (admin)
- **Ganho**: 1 VAL por mensagem (cooldown de 60s)

### Ranking de Holders NFT
- **Comando**: `/rankingholders` - Ranking on-chain dos holders
- **Detalhes**: Mostra alias, endereço e quantidade de NFTs
- **Agrupamento**: Por endereço com soma de balances
- **Metadata**: Nomes dos personagens dos tokens

### Comunicação
- **Comando**: `/talk` - Enviar mensagem para canal de anúncios
- **GM Automático**: Envio diário às 09:00 UTC
- **Mensagens**: Rotação automática de GMs

## 📁 Estrutura do Projeto

```
bl4clabot/
├── main.py                      # Bot principal
├── new_contract_utils.py        # Utilitários do novo contrato
├── fetch_new_contract_holders.py # Script standalone
├── test_new_contract.py         # Script de teste
├── keep_alive.py               # Manter bot ativo
├── tweets.txt                  # Mensagens GM
├── requirements.txt            # Dependências
├── .env                        # Variáveis de ambiente
└── README.md                   # Esta documentação
```

## 🛠️ Instalação

1. **Clone o repositório**
```bash
git clone <repository-url>
cd bl4clabot
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

4. **Execute o bot**
```bash
python main.py
```

## ⚙️ Configuração

### Variáveis de Ambiente (.env)
```env
DISCORD_TOKEN=seu_token_do_discord
DISCORD_GM_CHANNEL_ID=id_do_canal_gm
MONGODB_URI=sua_uri_mongodb
```

### Configurações do Bot
- **Prefix**: `/`
- **Moeda**: VALs
- **Ganho por mensagem**: 1 VAL
- **Cooldown**: 60 segundos
- **GM automático**: 09:00 UTC

## 📊 Comandos Disponíveis

### Para Usuários
- `/saldo [@usuario]` - Ver saldo de VALs
- `/posicao` - Ver ranking de VALs

### Para Administradores
- `/rankingholders` - Ranking de holders NFT
- `/darvals @usuario quantidade` - Adicionar VALs
- `/talk mensagem` - Enviar anúncio

## 🔧 Scripts Utilitários

### Testar Novo Contrato
```bash
python3 test_new_contract.py
```

### Buscar Holders Manualmente
```bash
python3 fetch_new_contract_holders.py
```

## 📈 Funcionalidades do Novo Contrato

### Estrutura dos Dados
- **Contrato**: FA2 (padrão Tezos para NFTs)
- **Tokens**: Cada token tem ID único e metadata rica
- **Holders**: Agrupamento por endereço com soma de balances
- **Alias**: Busca automática de aliases dos endereços

### Informações dos Tokens
- Nome do personagem
- District (bairro)
- Age (idade)
- Balaclava (cor)
- Background (cor de fundo)
- Member Since (membro desde)
- Item (item característico)

## 🎯 Vantagens do Novo Contrato

1. **Melhor Rastreamento** - Contrato dedicado facilita o rastreamento
2. **Metadata Rica** - Informações detalhadas sobre cada token
3. **Agrupamento Preciso** - Soma correta de NFTs por endereço
4. **Alias Automático** - Busca automática de nomes de usuários
5. **Detalhes dos Tokens** - Mostra quais NFTs cada holder possui

## 🔍 Verificação

Para verificar se tudo está funcionando:

1. Execute o teste: `python3 test_new_contract.py`
2. Use o comando no Discord: `/rankingholders`
3. Verifique os arquivos gerados: `new_contract_holders.csv` e `new_contract_holders.json`

## 📝 Arquivos de Saída

### CSV (`new_contract_holders.csv`)
```
Posição,Endereço,Alias,Quantidade Total,Tokens
1,tz1...,Nome,5,"Token1(ID:0); Token2(ID:1)"
```

### JSON (`new_contract_holders.json`)
```json
{
  "contract": "KT1JhZBNxoMB3QzcdJfopmq3R5R6jPiwC1nw",
  "total_holders": 85,
  "total_nfts": 85,
  "ranking": [...]
}
```

## 🎯 Próximos Passos

1. **Monitoramento** - Acompanhar crescimento da coleção
2. **Análises** - Criar relatórios de distribuição
3. **Integração** - Conectar com outros sistemas
4. **Automação** - Agendar atualizações periódicas

---

**Status**: ✅ Ativo e Funcionando  
**Última Atualização**: Dezembro 2024  
**Contrato**: `KT1JhZBNxoMB3QzcdJfopmq3R5R6jPiwC1nw`  
**Versão**: 2.0 - Novo Contrato 