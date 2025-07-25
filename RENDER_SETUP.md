# 🔧 Configuração do Render - Variáveis de Ambiente

## 🚨 **PROBLEMA IDENTIFICADO:**
O bot está offline no Render porque as **variáveis de ambiente** não estão configuradas.

## 📋 **Passos para Configurar:**

### **1. Acesse o Dashboard do Render:**
- Vá para [dashboard.render.com](https://dashboard.render.com)
- Faça login na sua conta

### **2. Selecione seu Serviço:**
- Clique no serviço `bl4clabot`
- Vá na aba **"Environment"**

### **3. Adicione as Variáveis de Ambiente:**

Clique em **"Add Environment Variable"** e adicione:

#### **🔑 DISCORD_TOKEN (OBRIGATÓRIO):**
```
Key: DISCORD_TOKEN
Value: [seu_token_do_discord_aqui]
```

#### **📺 DISCORD_GM_CHANNEL_ID:**
```
Key: DISCORD_GM_CHANNEL_ID
Value: 1333169997228281978
```

#### **📺 DISCORD_NEW_MEMBER_CHANNEL_ID:**
```
Key: DISCORD_NEW_MEMBER_CHANNEL_ID
Value: 1378199753484926976
```

#### **📺 DISCORD_ANNOUNCEMENT_CHANNEL_ID:**
```
Key: DISCORD_ANNOUNCEMENT_CHANNEL_ID
Value: 1333169997228281978
```

### **4. Salve as Configurações:**
- Clique em **"Save Changes"**
- O Render fará deploy automático

## 🎯 **Como Obter o DISCORD_TOKEN:**

### **Se você já tem o token:**
- Use o token que você já tem configurado

### **Se não tem o token:**
1. Acesse [Discord Developer Portal](https://discord.com/developers/applications)
2. Selecione sua aplicação BL4CL4
3. Vá em **"Bot"**
4. Clique em **"Reset Token"** ou copie o token existente
5. Cole no Render

## ✅ **Verificação:**

Após configurar:
1. **Aguarde o deploy** (2-5 minutos)
2. **Verifique os logs** no Render
3. **Teste no Discord:** `bl4ping`

## 🚨 **Logs Importantes:**

Procure por estas mensagens nos logs do Render:
- ✅ `"🤖 Bot conectado como BL4CL4#7466"`
- ✅ `"✅ Keep-alive ping realizado"`
- ❌ `"❌ DISCORD_TOKEN não encontrado"`

## 🔧 **Se Ainda Não Funcionar:**

1. **Verifique se o token está correto**
2. **Confirme se o bot está no servidor**
3. **Verifique as permissões do bot**
4. **Me envie os logs do Render**

---

**🎯 Resultado:** Bot online 24/7 no Render! 