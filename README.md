# AGT 4.0 - Relatório de Middleware e Infraestrutura

Sistema automatizado para análise de tickets de atendimento e geração de relatórios consolidados.

## Descrição

Este projeto processa tickets de suporte relacionados a Middleware, Infraestrutura e Database, gerando relatórios detalhados com análises por tipologia, módulo, origem e indicadores de performance.

## Estrutura do Projeto

```
primeiro-projeto-ai_python/
├── backend/
│   ├── app/
│   │   ├── services/          # Lógica de negócio
│   │   ├── models/            # Estruturas de dados
│   │   ├── utils/             # Utilitários
│   │   ├── reports/           # Geração de relatórios
│   │   ├── config.py          # Configurações
│   │   └── main.py            # Entrada principal
│   ├── tests/                 # Testes automatizados
│   ├── data/                  # Dados (input, processed, historical)
│   └── requirements.txt       # Dependências
├── docs/                      # Documentação
├── .env.example              # Variáveis de ambiente
└── README.md
```

## Instalação

1. Clone o repositório:
```bash
git clone <repo-url>
cd primeiro-projeto-ai_python
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r backend/requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```

## Uso

### Processamento Básico

```python
from backend.app.utils.csv_parser import ler_csv
from backend.app.services.ticket_service import TicketService
from backend.app.services.analysis_service import AnalysisService

# Carregar dados
dados = ler_csv('backend/data/input/tickets.csv')

# Processar tickets
service = TicketService()
service.carregar_tickets(dados)

# Gerar análises
resumo = AnalysisService.calcular_resumo_executivo(dados)
```

## Funcionalidades

### 1. Análise Executiva
- Total de tickets abertos/fechados
- Backlog final
- Comparativos mensais

### 2. Análise por Tipologia
- Incident, Support, Task
- Visão mensal e acumulada
- Comparativos

### 3. Análise por Módulo
- Database, PSRM, Portal, Batch Server, Jira Server, Clusters
- Distribuição por componentes
- Módulos com maior volume

### 4. Análise por Origem
- Middleware, Infraestrutura, Database, AD/BI
- Predominância de demandas

### 5. Indicadores
- Por tipologia
- Por módulo
- Por origem
- Cronológicos (evolução histórica)

## Formato de CSV de Entrada

O arquivo CSV deve conter as seguintes colunas:

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| ticket_id | string | ID único do ticket |
| titulo | string | Título/Assunto |
| descricao | string | Descrição detalhada |
| tipologia | string | Incident, Support, Task |
| origem | string | Middleware, Infraestrutura, Database, AD/BI |
| modulo | string | Database, PSRM, Portal, etc. |
| ambiente | string | Produção, Teste, Desenvolvimento |
| status | string | Aberto, Fechado, Em Progresso |
| data_abertura | date | Data de abertura (YYYY-MM-DD) |
| data_fechamento | date | Data de fechamento (YYYY-MM-DD) |
| assignee | string | Responsável |
| prioridade | string | Crítica, Alta, Média, Baixa |

## Testes

Execute os testes com:

```bash
pytest backend/tests/ -v --cov=backend/app
```

## Contribuição

1. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
2. Faça commit das mudanças (`git commit -m 'Adiciona MinhaFeature'`)
3. Push para a branch (`git push origin feature/MinhaFeature`)
4. Abra um Pull Request

## Licença

Este projeto está sob licença MIT.

## Contato

Para dúvidas ou sugestões, entre em contato.
