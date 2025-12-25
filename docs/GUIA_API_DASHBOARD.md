# AGT 4.0 - Guia de Uso: API REST e Dashboard

## 🚀 Início Rápido

### Instalação de Dependências

```bash
pip install -r backend/requirements.txt
```

---

## 📊 Dashboard Streamlit

### Iniciar o Dashboard

```bash
streamlit run backend/dashboard.py
```

Acessar em: **http://localhost:8501**

### Funcionalidades

#### 1. **Análise de um Período** 📈
- Upload de arquivo CSV do Jira
- Visualização imediata de métricas
- Tabelas e gráficos interativos
- Download de relatório PDF com gráficos

#### 2. **Comparativo Entre Períodos** 📊
- Upload de dois arquivos CSV (anterior e atual)
- Comparação lado a lado de métricas
- Cálculo automático de variações
- Relatório PDF comparativo com gráficos

### Características
- ✅ Interface intuitiva e responsiva
- ✅ Visualizações em tempo real
- ✅ Suporte a múltiplos formatos de entrada
- ✅ Download de PDFs em um clique
- ✅ Gráficos de barras, pizza e métricas

---

## 🌐 API REST - FastAPI

### Iniciar a API

```bash
python -m uvicorn backend.app.api:app --reload --host 0.0.0.0 --port 8000
```

Ou simplesmente:

```bash
python backend/app/api.py
```

Acessar em: **http://localhost:8000**

Documentação Swagger: **http://localhost:8000/docs**

### Endpoints

#### 1. **GET /health** ✅
Verificar saúde da API

**Request:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "OK",
  "servico": "AGT 4.0 API"
}
```

---

#### 2. **POST /upload-csv** 📤
Upload de um arquivo CSV e geração de relatório

**Request:**
```bash
curl -X POST "http://localhost:8000/upload-csv" \
  -F "file=@JIRAS_NOV2025_formatado.csv"
```

**Response:**
```json
{
  "status": "sucesso",
  "arquivo": "JIRAS_NOV2025_formatado.csv",
  "total_tickets": 43,
  "resumo": {
    "total_abertos": 0,
    "total_fechados": 43,
    "total_geral": 43,
    "backlog_final": 0
  },
  "pdf_path": "/caminho/para/relatorio.pdf",
  "pdf_url": "/download/relatorio_JIRAS_NOV2025_formatado.pdf"
}
```

---

#### 3. **POST /upload-comparativo** 📊
Upload de dois arquivos CSV para comparação

**Request:**
```bash
curl -X POST "http://localhost:8000/upload-comparativo" \
  -F "arquivo_anterior=@JIRAS_OUT2025_formatado.csv" \
  -F "arquivo_atual=@JIRAS_NOV2025_formatado.csv"
```

**Response:**
```json
{
  "status": "sucesso",
  "arquivo_anterior": "JIRAS_OUT2025_formatado.csv",
  "arquivo_atual": "JIRAS_NOV2025_formatado.csv",
  "tickets_anterior": 66,
  "tickets_atual": 43,
  "comparativo": {
    "periodo_anterior": "OUT2025",
    "periodo_atual": "NOV2025",
    "total_anterior": 66,
    "total_atual": 43,
    "variacao_total": -23,
    "abertos_anterior": 7,
    "abertos_atual": 0,
    "variacao_abertos": -7,
    "fechados_anterior": 59,
    "fechados_atual": 43,
    "variacao_fechados": -16,
    "backlog_anterior": 7,
    "backlog_atual": 0,
    "variacao_backlog": -7
  },
  "pdf_path": "/caminho/para/relatorio_comparativo.pdf",
  "pdf_url": "/download/relatorio_comparativo_OUT2025_vs_NOV2025.pdf"
}
```

---

#### 4. **GET /download/{filename}** ⬇️
Download de arquivo PDF gerado

**Request:**
```bash
curl -O http://localhost:8000/download/relatorio_JIRAS_NOV2025_formatado.pdf
```

---

## 📝 Exemplos de Uso Completo

### Usando o Dashboard (Recomendado para Usuários)

1. Abrir: `http://localhost:8501`
2. Selecionar "Análise de Período"
3. Fazer upload de CSV
4. Nomear o período
5. Visualizar análises interativas
6. Clicar em "Gerar PDF com Gráficos"
7. Download automático do PDF

### Usando a API (Recomendado para Integrações)

**Script Python:**
```python
import requests

# Upload simples
with open('JIRAS_NOV2025_formatado.csv', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/upload-csv', files=files)
    print(response.json())

# Upload comparativo
with open('JIRAS_OUT2025_formatado.csv', 'rb') as f1, \
     open('JIRAS_NOV2025_formatado.csv', 'rb') as f2:
    files = {
        'arquivo_anterior': f1,
        'arquivo_atual': f2
    }
    response = requests.post('http://localhost:8000/upload-comparativo', files=files)
    print(response.json())

# Download
response = requests.get('http://localhost:8000/download/relatorio.pdf')
with open('relatorio.pdf', 'wb') as f:
    f.write(response.content)
```

---

## 🎨 Características dos Relatórios PDF

### Conteúdo

1. **Header Personalizado**
   - Título: "RELATÓRIO DE MIDDLEWARE E INFRAESTRUTURA"
   - Subtítulo: "AGT 4.0"
   - Período e data/hora de geração

2. **Seção 1: Resumo Executivo**
   - Total de tickets
   - Abertos, fechados e backlog
   - Tabela formatada

3. **Seção 2: Análise por Tipologia**
   - Tabela com contagens
   - Gráfico de pizza com percentuais

4. **Seção 3: Análise por Componente**
   - Tabela com contagens
   - Gráfico de barras

5. **Seção 4: Análise por Origem**
   - Tabela com contagens
   - Gráfico de barras

6. **Seção 5: Análise por Prioridade**
   - Tabela com contagens
   - Gráfico de barras

7. **Seção 6 (Se Comparativo): Comparação de Períodos**
   - Tabela com variações
   - Análise de tendências

### Design
- Layout: A4 Landscape
- Cores corporativas: Azul #1f4788
- Tabelas coloridas com bordas
- Gráficos legíveis
- Fontes profissionais

---

## 🔧 Arquivos Importantes

| Arquivo | Descrição |
|---------|-----------|
| `backend/dashboard.py` | Dashboard Streamlit |
| `backend/app/api.py` | API REST FastAPI |
| `backend/app/services/pdf_report_service.py` | Gerador de PDFs com gráficos |
| `backend/app/services/analysis_service.py` | Análises de dados |
| `backend/app/utils/jira_parser.py` | Parser de CSV Jira |
| `backend/requirements.txt` | Dependências Python |

---

## 📊 Estrutura de Saída

```
backend/app/reports/output/
├── relatorio_AGT40_Outubro_2025.pdf
├── relatorio_AGT40_Novembro_2025.pdf
├── relatorio_AGT40_Comparativo_OutNov_2025.pdf
├── relatorio_AGT40_Novembro_Com_Graficos.pdf
└── ...
```

---

## ⚠️ Troubleshooting

### Erro: "Módulo não encontrado"
```bash
pip install -r backend/requirements.txt
```

### Erro: "Porta 8501 em uso"
```bash
streamlit run backend/dashboard.py --server.port 8502
```

### Erro: "Porta 8000 em uso"
```bash
python -m uvicorn backend.app.api:app --port 8001
```

### Erro ao gerar PDF
- Certifique-se que reportlab está instalado: `pip install reportlab matplotlib`
- Verifique permissões de escrita no diretório de saída

---

## 🚀 Próximos Passos

- [ ] Adicionar histórico de 12 meses
- [ ] Integração com banco de dados
- [ ] Agendamento automático de relatórios
- [ ] Envio de relatórios por email
- [ ] Dashboard com mais gráficos avançados
- [ ] Autenticação e controle de acesso
- [ ] Cache de resultados

---

## 📞 Contato e Suporte

Para dúvidas ou sugestões sobre o sistema, entre em contato.

**Versão**: 1.0.0  
**Data**: 24/12/2025  
**Desenvolvido com**: Python, FastAPI, Streamlit, ReportLab
