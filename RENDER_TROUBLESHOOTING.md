# Guia de Solução de Problemas - Render.com

## Problema: Bot aparece offline no Discord mas está rodando no Render

### 🔍 **Diagnóstico**

1. **Verificar logs no Render**:
   - Acesse o dashboard do Render
   - Vá em "Logs" do seu serviço
   - Procure por erros de conexão

2. **Verificar variáveis de ambiente**:
   - `DISCORD_TOKEN` está configurado?
   - `DISCORD_GM_CHANNEL_ID` está correto?

### 🛠️ **Soluções**

#### 1. **Usar a versão otimizada para Render**
```bash
# Use o arquivo main_render.py em vez de main_clean.py
python3 main_render.py
```

#### 2. **Configurar variáveis de ambiente no Render**
No dashboard do Render, configure:
```
DISCORD_TOKEN=seu_token_aqui
DISCORD_GM_CHANNEL_ID=1333169997228281978
```

#### 3. **Verificar permissões do bot**
O bot precisa das seguintes permissões:
- ✅ Ler Mensagens
- ✅ Enviar Mensagens
- ✅ Gerenciar Mensagens
- ✅ Ver Canais

#### 4. **Verificar intents no Discord Developer Portal**
1. Acesse https://discord.com/developers/applications
2. Selecione sua aplicação
3. Vá em "Bot"
4. Habilite os intents necessários:
   - Message Content Intent
   - Server Members Intent (se necessário)

### 📋 **Checklist de Verificação**

- [ ] Bot está rodando no Render
- [ ] Variáveis de ambiente configuradas
- [ ] Token do Discord válido
- [ ] Intents habilitados no Developer Portal
- [ ] Bot tem permissões no servidor
- [ ] Bot está no servidor correto

### 🔧 **Comandos de Teste**

#### Testar conectividade:
```bash
curl https://seu-app.onrender.com/health
```

#### Verificar logs:
```bash
# No Render dashboard > Logs
```

### 📝 **Logs Importantes**

Procure por estas mensagens nos logs:
- `"🤖 Bot conectado como"`
- `"⚠️ Bot desconectado do Discord"`
- `"🔄 Bot reconectado ao Discord"`
- `"✅ Keep-alive ping realizado"`

### 🚨 **Problemas Comuns**

#### 1. **Token inválido**
```
Erro: 401 Unauthorized
```
**Solução**: Verificar se o token está correto

#### 2. **Intents não habilitados**
```
discord.errors.PrivilegedIntentsRequired
```
**Solução**: Habilitar intents no Developer Portal

#### 3. **Bot não está no servidor**
```
discord.errors.Forbidden: 403 Forbidden
```
**Solução**: Convidar o bot para o servidor

#### 4. **Timeout de conexão**
```
discord.errors.ConnectionClosed
```
**Solução**: Usar a versão `main_render.py` com keep-alive

### 🔄 **Reiniciar o Serviço**

1. No dashboard do Render
2. Vá em seu serviço
3. Clique em "Manual Deploy"
4. Selecione "Clear build cache & deploy"

### 📞 **Suporte**

Se os problemas persistirem:
1. Verifique os logs completos no Render
2. Teste localmente primeiro
3. Verifique se o token não foi regenerado
4. Confirme se o bot não foi removido do servidor 