# Guia de Solução de Problemas - Comando /talk

## Problemas Comuns e Soluções

### 1. Bot não responde ao comando /talk

**Possíveis causas:**
- Bot não está online
- Prefixo incorreto (deve ser `/`)
- Bot não tem permissões para ler mensagens

**Soluções:**
```bash
# Verificar se o bot está rodando
python3 main.py

# Verificar logs
tail -f bot.log
```

### 2. Erro: "Você não tem permissão para usar este comando"

**Causa:** Usuário não tem cargo de administrador

**Solução:**
- Adicionar cargo de administrador ao usuário no Discord
- Ou modificar o código para usar outro cargo específico

### 3. Erro: "Este comando só pode ser usado em #canal"

**Causa:** Comando sendo usado no canal errado

**Solução:**
- Usar o comando apenas no canal com ID: `1378199753484926976`
- Verificar se o ID do canal está correto no código

### 4. Erro: "Canal de anúncios não encontrado"

**Causa:** ID do canal de anúncios incorreto ou bot sem acesso

**Solução:**
- Verificar se o ID `1333169997228281978` está correto
- Garantir que o bot tenha acesso ao canal
- Verificar se o bot está no servidor correto

### 5. Erro: "Bot sem permissão para enviar mensagens"

**Causa:** Bot não tem permissões no canal de destino

**Solução:**
- Dar permissão "Enviar Mensagens" ao bot no canal de anúncios
- Verificar permissões do cargo do bot

### 6. Bot não consegue deletar mensagens

**Causa:** Bot sem permissão "Gerenciar Mensagens"

**Solução:**
- Adicionar permissão "Gerenciar Mensagens" ao bot

## Como Testar

### 1. Usar o script de teste
```bash
python3 test_talk_command.py
```

### 2. Verificar configurações
```python
# Verificar se estas variáveis estão corretas
DISCORD_NEW_MEMBER_CHANNEL_ID = 1378199753484926976
DISCORD_ANNOUNCEMENT_CHANNEL_ID = 1333169997228281978
```

### 3. Verificar permissões do bot
O bot precisa das seguintes permissões:
- ✅ Ler Mensagens
- ✅ Enviar Mensagens
- ✅ Gerenciar Mensagens (para deletar comandos)
- ✅ Ver Canais

## Comandos Úteis

### Verificar status do bot
```bash
# Ver logs em tempo real
tail -f bot.log | grep -i talk

# Verificar se o bot está rodando
ps aux | grep python
```

### Reiniciar o bot
```bash
# Parar o bot (Ctrl+C)
# Iniciar novamente
python3 main.py
```

## Estrutura do Comando

```python
@bot.command()
@commands.has_permissions(administrator=True)
async def talk(ctx, *, mensagem):
    # 1. Verificar canal correto
    # 2. Deletar mensagem original
    # 3. Verificar canal de destino
    # 4. Verificar permissões
    # 5. Enviar mensagem
    # 6. Confirmar envio
```

## Logs Importantes

Procure por estas mensagens no `bot.log`:
- `"Mensagem enviada via /talk por"`
- `"Erro no comando /talk"`
- `"Canal de anúncios não encontrado"`
- `"Bot sem permissão para enviar mensagens"`

## Contato

Se os problemas persistirem, verifique:
1. Logs do bot (`bot.log`)
2. Permissões no Discord
3. IDs dos canais
4. Status do bot 