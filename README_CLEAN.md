# Bot Discord BL4CL4 - Versão Limpa

Bot simples e focado para o servidor Discord BL4CL4.

## Funcionalidades

### 🗣️ Comando `/talk`
- **Uso**: `/talk <mensagem>`
- **Permissão**: Apenas administradores
- **Canal**: Deve ser usado no canal específico
- **Função**: Envia mensagem para o canal de anúncios

### 🌅 GM Diário
- **Horário**: 09:00 UTC todos os dias
- **Função**: Envia mensagem GM aleatória da lista
- **Canal**: Configurado via `DISCORD_GM_CHANNEL_ID`

### 🔧 Comandos Adicionais
- `/ping` - Teste de conectividade
- `/gm` - Enviar GM manualmente (apenas admins)
- `/status` - Status do bot

## Instalação

1. **Instalar dependências**:
```bash
pip install -r requirements_clean.txt
```

2. **Configurar arquivo `.env`**:
```bash
cp env_clean.example .env
# Editar .env com suas configurações
```

3. **Executar o bot**:
```bash
python3 main_clean.py
```

## Configuração

### Variáveis de Ambiente (`.env`)
```env
DISCORD_TOKEN=seu_token_aqui
DISCORD_GM_CHANNEL_ID=id_do_canal_gm
```

### IDs dos Canais (já configurados)
- **Canal de comando**: `1378199753484926976`
- **Canal de anúncios**: `1333169997228281978`

## Permissões Necessárias

O bot precisa das seguintes permissões:
- ✅ Ler Mensagens
- ✅ Enviar Mensagens
- ✅ Gerenciar Mensagens
- ✅ Ver Canais

## Logs

Os logs são salvos em `bot.log` e também exibidos no console.

## Estrutura do Projeto

```
bl4clabot/
├── main_clean.py          # Bot principal (versão limpa)
├── requirements_clean.txt # Dependências
├── env_clean.example     # Exemplo de configuração
├── README_CLEAN.md       # Este arquivo
└── bot.log              # Logs do bot
```

## Comandos

| Comando | Descrição | Permissão |
|---------|-----------|-----------|
| `/talk <msg>` | Enviar mensagem para anúncios | Admin |
| `/ping` | Teste de conectividade | Todos |
| `/gm` | Enviar GM manualmente | Admin |
| `/status` | Status do bot | Todos |

## Suporte

Para problemas ou dúvidas, verifique:
1. Logs em `bot.log`
2. Permissões do bot no Discord
3. Configuração do arquivo `.env` 