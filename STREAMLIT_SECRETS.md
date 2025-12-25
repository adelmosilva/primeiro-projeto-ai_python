# 🔐 Configurar Secrets no Streamlit Cloud

Após criar o projeto no Supabase, você precisa adicionar as credenciais ao Streamlit Cloud.

## 1️⃣ Acessar Secrets do App

1. Vá para sua aplicação no Streamlit Cloud
2. Clique em **"⋮"** (três pontos) no canto superior direito
3. Selecione **"Edit secrets"**

---

## 2️⃣ Adicionar as Credenciais do Supabase

Cole o seguinte no campo de secrets (TOML format):

### **Opção A: Usando Connection String Completa** (Recomendado)

```toml
SUPABASE_URL = "postgresql://user.xxxxx:password@host.supabase.co:5432/postgres"
SUPABASE_PASSWORD = "sua_senha_aqui"
```

### **Opção B: Dados Individuais**

```toml
SUPABASE_HOST = "aws-0-sa-east-1.db.supabase.co"
SUPABASE_PORT = 5432
SUPABASE_USER = "postgres.xxxxx"
SUPABASE_PASSWORD = "sua_senha"
SUPABASE_DB = "postgres"
```

---

## 3️⃣ Obter Informações do Supabase

1. Vá para seu projeto no Supabase
2. **Settings** > **Database**
3. Encontre a seção **Connection String**

A string fica assim:
```
postgresql://postgres.xxxxx:password@aws-0-sa-east-1.db.supabase.co:5432/postgres
```

Extraia:
- **User**: `postgres.xxxxx` (antes do `:`)
- **Password**: tudo entre `:` e `@`
- **Host**: `aws-0-sa-east-1.db.supabase.co`

---

## ✅ Salvar Secrets

1. Cole as informações no editor de secrets
2. Clique em **"Save"**
3. Seu app vai fazer refresh automaticamente

---

## 🧪 Testar Conexão

Acesse sua dashboard e verifique se conectou ao banco. Se funcionar:
- ✅ Dados carregados normalmente
- ❌ Se não funcionar: Verifique as credenciais

---

## 📝 Checklist

- [ ] Criei projeto no Supabase?
- [ ] Copiei a Connection String?
- [ ] Adicionei os secrets no Streamlit Cloud?
- [ ] Fiz refresh da aplicação?

Depois disso, tudo deve funcionar! 🚀
