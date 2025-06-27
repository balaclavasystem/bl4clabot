# 🗄️ Configuração MongoDB Atlas - Guia Completo

## Por que migrar para MongoDB?

- ✅ **Dados persistentes** - Não perde dados quando o servidor reinicia
- ✅ **Gratuito** - MongoDB Atlas tem plano gratuito generoso
- ✅ **Seguro** - Backup automático e criptografia
- ✅ **Escalável** - Suporta milhões de usuários
- ✅ **Acessível de qualquer lugar** - Dados na nuvem

## 📋 Passo a Passo

### 1. Criar conta no MongoDB Atlas

1. Acesse [mongodb.com/atlas](https://mongodb.com/atlas)
2. Clique em "Try Free"
3. Preencha seus dados e crie uma conta
4. Escolha o plano **FREE** (M0)

### 2. Criar Cluster

1. Clique em "Build a Database"
2. Escolha "FREE" tier
3. Escolha um provedor (AWS, Google Cloud, ou Azure)
4. Escolha uma região (preferencialmente próxima ao Brasil)
5. Clique em "Create"

### 3. Configurar Acesso

1. **Criar usuário do banco:**
   - Username: `bl4clabot`
   - Password: `sua_senha_segura_123`
   - Clique em "Create User"

2. **Configurar IP:**
   - Clique em "Network Access"
   - Clique em "Add IP Address"
   - Clique em "Allow Access from Anywhere" (0.0.0.0/0)
   - Clique em "Confirm"

### 4. Obter String de Conexão

1. Clique em "Database" no menu lateral
2. Clique em "Connect"
3. Escolha "Connect your application"
4. Copie a string de conexão

A string será algo como:
```
mongodb+srv://bl4clabot:sua_senha_segura_123@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

### 5. Configurar Variável de Ambiente

1. No Render, vá nas configurações do seu projeto
2. Adicione uma nova variável de ambiente:
   - **Key:** `MONGODB_URI`
   - **Value:** `mongodb+srv://bl4clabot:sua_senha_segura_123@cluster0.xxxxx.mongodb.net/bl4clabot?retryWrites=true&w=majority`

**IMPORTANTE:** Substitua `sua_senha_segura_123` pela senha que você criou e `cluster0.xxxxx.mongodb.net` pela URL do seu cluster.

### 6. Deploy no Render

1. Faça commit das mudanças no GitHub
2. O Render vai fazer deploy automaticamente
3. Verifique os logs para confirmar que conectou no MongoDB

### 7. Migrar Dados Existentes (Opcional)

Se você já tem dados no arquivo `saldos.json`:

1. Execute o script de migração:
```bash
python migrate_to_mongodb.py
```

## 🔧 Testando

1. Envie uma mensagem no Discord
2. Use `/saldo` para verificar se ganhou VALs
3. Use `/rank` para ver o ranking
4. Verifique os logs do Render para confirmar que está salvando no MongoDB

## 🚨 Troubleshooting

### Erro de conexão
- Verifique se a string de conexão está correta
- Confirme se o IP está liberado no MongoDB Atlas
- Verifique se o usuário e senha estão corretos

### Bot não responde
- Verifique os logs no Render
- Confirme se a variável `MONGODB_URI` está configurada
- Reinicie o serviço no Render

## 📊 Benefícios

- **Dados seguros** - Backup automático a cada 6 horas
- **Sempre online** - 99.95% de uptime
- **Monitoramento** - Dashboard com estatísticas
- **Escalável** - Suporta crescimento do servidor

## 🎯 Próximos Passos

Após a migração, você pode:
- Adicionar mais comandos de economia
- Implementar sistema de apostas
- Criar loja de itens
- Adicionar sistema de transferência entre usuários

---

**Precisa de ajuda?** Verifique os logs do Render ou me avise! 