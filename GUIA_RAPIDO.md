# 🚀 GUIA RÁPIDO - Sistema de Relatórios Comparativos

## ⚡ Início Rápido (3 passos)

### 1️⃣ **Inicie o Dashboard**
```bash
cd backend
streamlit run dashboard.py
```
Abre em: `http://localhost:8501`

### 2️⃣ **No Dashboard - Modo Comparativo**
- Navegue para **"Comparativo"**
- Upload de 2 CSVs (período anterior e período atual)
- Verá automaticamente as **3 novas análises**:
  - 📊 Distribuição por Tipologia (5 tabelas)
  - 📊 Top 10 Módulos/Servidores (10 tabelas)
  - 📊 Análise por Origem com % (6 tabelas)
- Clique em **"Gerar PDF Comparativo"**

### 3️⃣ **Baixe o PDF**
PDF será salvo automaticamente em: `relatorios/`

---

## 📊 Novas Análises Implementadas

### ✅ **Análise por Tipologia** (7 colunas)
Agrupa tickets por tipo (Epic, Incident, Iniciativa, Support, Task)
```
Tipologia    | Abertos Ant | Abertos Atu | Fechados Ant | Fechados Atu | Total Ant | Total Atu
Support      | 0           | 0           | 200          | 150          | 205       | 150
Incident     | 1           | 0           | 100          | 80           | 101       | 80
Task         | 10          | 10          | 500          | 400          | 510       | 410
```

### ✅ **Top 10 Módulos** (5 colunas)
Servidores/Clusters com mais tickets
```
Módulo           | Abertos Ant | Abertos Atu | Fechados Ant | Fechados Atu
Batch Server     | 100         | 80          | 500          | 400
PSRM             | 50          | 40          | 300          | 250
DataBase         | 10          | 5           | 200          | 180
```

### ✅ **Análise por Origem** (9 colunas)
Distribuição com percentuais calculados
```
Origem       | Abertos Ant | Abertos Atu | Fechados Ant | Fechados Atu | Total Ant | Total Atu | % Ant | % Atu
Database     | 10          | 5           | 200          | 180          | 258       | 180       | 57.0% | 59.6%
Middleware   | 100         | 95          | 500          | 400          | 645       | 300       | 85.7% | 82.5%
Infra        | 5           | 2           | 100          | 90           | 120       | 100       | 3.6%  | 2.5%
```

---

## 🔌 Via API REST

**Endpoint**: `POST /upload-comparativo`

```bash
curl -X POST http://localhost:8000/upload-comparativo \
  -F "arquivo_anterior=@JIRAS_OUT2025_formatado.csv" \
  -F "arquivo_atual=@JIRAS_NOV2025_formatado.csv"
```

**Resposta**: Arquivo PDF com:
- 10 seções originais (análises básicas)
- **3 novas seções** (tabelas detalhadas)

---

## 📁 Estrutura de Arquivos

```
projeto/
├── backend/
│   ├── app/
│   │   ├── services/
│   │   │   ├── analysis_service.py      ← 4 novos métodos
│   │   │   └── pdf_report_service.py    ← 3 novas seções
│   │   └── api.py                       ← Integrado
│   └── dashboard.py                     ← Integrado com tabelas
├── uploads/                             ← Coloque CSVs aqui
├── relatorios/                          ← PDFs salvos aqui
├── IMPLEMENTACAO_FINAL.md               ← Documentação completa
├── test_novos_metodos.py               ← Testes (todos passam ✅)
├── test_pdf_completo.py                ← Teste de PDF (✅)
├── test_api_comparativo.py             ← Teste da API (✅)
└── status_report.py                    ← Relatório de status
```

---

## 🧪 Testar Implementação

```bash
# Teste 1: Validar métodos de análise
python test_novos_metodos.py

# Teste 2: Gerar PDF completo
python test_pdf_completo.py

# Teste 3: Simular chamada da API
python test_api_comparativo.py

# Teste 4: Ver relatório de status
python status_report.py
```

**Resultado esperado**: ✅ Todos os testes passam

---

## 💡 Características

✅ **Comparativo Automático**: Compara 2 períodos automaticamente  
✅ **Percentuais**: Calculados automaticamente para Origem  
✅ **Formatação**: Tabelas com cores diferentes no PDF  
✅ **Interativo**: Tabelas no Dashboard são responsivas  
✅ **Flexível**: Funciona com qualquer CSV formatado  
✅ **Integrado**: Works with API + Dashboard + PDF  

---

## 📋 Mapeamento de Origem

Como os componentes são mapeados para origens:

| Componente | Origem |
|-----------|--------|
| Database | Database |
| AD/BI | AD/BI |
| Middleware | Middleware |
| Infraestruturas | Infra |
| MFT Server | MFT |
| (vazio) | Não especificado |

---

## ⚠️ Requisitos

- Python 3.8+
- Pandas 2.1.0+
- ReportLab 4.0.0+
- FastAPI 0.100.0+
- Streamlit 1.28.0+

```bash
pip install pandas reportlab fastapi streamlit
```

---

## 🔧 Troubleshooting

### ❓ **"File not found" ao carregar CSV**
→ Coloque o arquivo em `uploads/` folder

### ❓ **PDF não contém tabelas**
→ Verifique se CSVs estão formatados corretamente

### ❓ **Dashboard não abre**
→ Execute: `streamlit run backend/dashboard.py`

### ❓ **Percentuais zerados na Origem**
→ Verifique se há tickets com componente "Não especificado"

---

## 📞 Contato & Suporte

Ver arquivo: `IMPLEMENTACAO_FINAL.md` para documentação completa.

---

## 📊 Exemplo de Output

Ao gerar um PDF, você verá:

```
RELATÓRIO COMPARATIVO - OUTUBRO vs NOVEMBRO 2025

1. RESUMO EXECUTIVO
2. ANÁLISE POR TIPOLOGIA (gráfico)
3. ANÁLISE POR COMPONENTE (gráfico)
...
10. TOP 10 SERVIDORES
11. ✨ ANÁLISE POR TIPOLOGIA (TABELA)
12. ✨ TOP 10 MÓDULOS (TABELA)
13. ✨ ANÁLISE POR ORIGEM (TABELA)
```

As 3 seções com ✨ são novas!

---

**Status**: ✅ Pronto para Produção  
**Data**: Dezembro 2025  
**Versão**: 1.0 - Implementação Completa
