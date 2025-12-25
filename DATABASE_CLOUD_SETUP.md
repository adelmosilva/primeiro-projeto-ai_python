# 🌐 Configuração do Banco de Dados para Streamlit Cloud

## ❌ Problema Atual

O banco de dados está em um servidor privado (91.108.124.150) acessível apenas via SSH. O Streamlit Cloud não consegue:
- ✗ Acessar redes privadas
- ✗ Usar SSH tunnels diretos
- ✗ Carregar chaves SSH do repositório

---

## ✅ Soluções Disponíveis

### **Opção 1: Usar Banco de Dados em Nuvem (Recomendado)**

Migrar o PostgreSQL para um serviço gerenciado com URL pública:

**Provedores:**
- **Heroku PostgreSQL** (gratuito com limitações)
- **Render.com** (gratuito até 90 dias)
- **Neon** (PostgreSQL serverless, gratuito)
- **Supabase** (PostgreSQL gerenciado, gratuito)
- **PlanetScale** (MySQL alternativa)

**Passos:**
1. Criar conta no provedor escolhido
2. Obter URL de conexão pública
3. Atualizar `env_config.py` com a URL
4. Remover dependência de SSH

---

### **Opção 2: SSH Tunnel via ngrok (Proxy Público)**

Expor o banco privado via tunnel público:

**Passos:**
1. Instalar ngrok: https://ngrok.com/download
2. Criar tunnel: `ngrok tcp 5432`
3. Obter URL pública (ex: `0.tcp.ngrok.io:12345`)
4. Configurar credenciais de ngrok no Streamlit Cloud (Secrets)
5. Usar a URL pública no código

---

### **Opção 3: API Intermediária (Melhor Prática)**

Criar uma API REST entre Streamlit Cloud e o banco privado:

```
Streamlit Cloud
      ↓ HTTP/HTTPS
   API REST (FastAPI)
      ↓ SSH Tunnel
PostgreSQL (privado)
```

**Benefícios:**
- ✅ Segurança melhorada
- ✅ Controle de acesso
- ✅ Cache de dados
- ✅ Rate limiting

---

## 🔐 Como Funciona Localmente

Atualmente, o código detecta se está rodando localmente e usa SSH tunnel:

```python
IS_STREAMLIT_CLOUD = 'STREAMLIT' in os.environ

if IS_STREAMLIT_CLOUD:
    # Conectar via URL pública
    usar_conexao_cloud()
else:
    # Conectar via SSH tunnel (local)
    usar_ssh_tunnel()
```

---

## 📋 Próximos Passos

**Escolha uma opção acima e avise qual você prefere.**

Vou então:
1. Configurar a conexão apropriada
2. Adicionar secrets do Streamlit Cloud (se necessário)
3. Testar a conexão
4. Fazer deploy atualizado

---

## 🚀 Atalho Rápido: Usar Supabase (Gratuito)

1. Vá para: https://supabase.com
2. Clique "Start your project"
3. Criar projeto (leva ~1 min)
4. Copiar URL de conexão PostgreSQL
5. Compartilhar comigo!

Depois eu configuro automaticamente no código.
