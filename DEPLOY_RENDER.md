# 🚀 Deploy do Bot BL4CL4 no Render

## 📋 **Passos para Deploy Automático 24/7**

### **1. Preparar o Repositório**
```bash
# Certifique-se de que todos os arquivos estão commitados
git add .
git commit -m "Preparando deploy no Render"
git push origin main
```

### **2. Conectar ao Render**
1. Acesse [render.com](https://render.com)
2. Faça login ou crie uma conta
3. Clique em "New" → "Web Service"
4. Conecte seu repositório GitHub

### **3. Configurar o Serviço**
- **Name:** `bl4cl4-bot`
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements_render.txt`
- **Start Command:** `python3 main_render.py`
- **Plan:** `Free`

### **4. Configurar Variáveis de Ambiente**
No dashboard do Render, adicione:
```
DISCORD_TOKEN=seu_token_do_discord_aqui
DISCORD_GM_CHANNEL_ID=1333169997228281978
```

### **5. Deploy Automático**
- O Render detectará o arquivo `render.yaml`
- Fará deploy automático
- Bot ficará online 24/7

## ✅ **Vantagens do Render**

### **🔄 Auto-restart**
- Reinicia automaticamente se cair
- Mantém o bot sempre online

### **📊 Monitoramento**
- Logs em tempo real
- Status de saúde do serviço
- Alertas automáticos

### **💰 Gratuito**
- Plano free disponível
- Sem custos mensais

### **🌐 Acesso Global**
- Servidor sempre disponível
- Não depende do seu computador

## 🔧 **Verificação Pós-Deploy**

### **1. Verificar Status**
- Dashboard do Render mostra "Live"
- Logs mostram "Bot conectado"

### **2. Testar Comandos**
No Discord, teste:
```
!ping
!status
!gm
```

### **3. Monitorar Logs**
- Acesse "Logs" no Render
- Procure por mensagens de sucesso

## 🚨 **Problemas Comuns**

### **Bot Offline**
- Verificar variáveis de ambiente
- Verificar logs no Render
- Verificar token do Discord

### **Comandos Não Funcionam**
- Verificar permissões do bot
- Verificar intents no Developer Portal
- Verificar prefixo dos comandos

## 📞 **Suporte**
- Render Dashboard: Logs e status
- Discord Developer Portal: Configurações do bot
- GitHub: Código fonte e issues

---

**🎯 Resultado:** Bot online 24/7 sem precisar manter seu computador ligado! 