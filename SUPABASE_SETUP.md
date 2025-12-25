# 🚀 Setup do Supabase - Passo a Passo

## 1️⃣ Criar Conta no Supabase

1. Vá para: https://supabase.com
2. Clique em **"Start your project"** ou **"Sign up"**
3. Use sua conta Google/GitHub para criar a conta

---

## 2️⃣ Criar Novo Projeto

1. Clique em **"New project"**
2. Preencha:
   - **Project name**: `agt-4-0` (ou outro nome)
   - **Database password**: Crie uma senha forte (salve em local seguro!)
   - **Region**: `São Paulo (sa-east-1)` (mais próximo)
3. Clique em **"Create new project"** e aguarde (~2 minutos)

---

## 3️⃣ Obter Credenciais

Após criar o projeto:

1. Vá para **Settings** (engrenagem no menu lateral)
2. Clique em **"Database"**
3. Copie a informação abaixo (você vai precisar):

```
Connection String (PostgreSQL):
postgresql://postgres.XXXXXXXXXX:PASSWORD@aws-0-sa-east-1.db.supabase.co:5432/postgres
```

Ou se preferir, use as informações individuais:
- **Host**: `aws-0-sa-east-1.db.supabase.co`
- **Port**: `5432`
- **Database**: `postgres`
- **User**: `postgres.XXXXXXXXXX`
- **Password**: A senha que você criou

---

## 4️⃣ Obter API Key (Opcional, mas recomendado)

1. Vá para **Settings** > **API**
2. Copie a **anon public** (para segurança, se usar)

---

## 5️⃣ Criar Tabela no Supabase (Se necessário)

Se estiver migrando dados:

1. Vá para **SQL Editor** no Supabase
2. Cole o SQL da sua tabela (vou preparar para você)
3. Clique em **"Run"**

---

## 📋 Informações Necessárias para Configurar

Assim que tiver o Supabase criado, **me passe:**

```
SUPABASE_HOST: aws-0-sa-east-1.db.supabase.co (exemplo)
SUPABASE_USER: postgres.xxxxx
SUPABASE_PASSWORD: sua_senha
SUPABASE_DB: postgres
```

Ou simplesmente compartilhe a **Connection String** completa!

---

## ⏱️ Tempo Estimado
- Criar conta: 2 minutos
- Criar projeto: 2 minutos
- Copiar credenciais: 1 minuto

**Total: ~5 minutos** ⚡

---

Assim que tiver as credenciais, eu configuro tudo automaticamente!
