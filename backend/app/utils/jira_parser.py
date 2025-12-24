"""
Parser específico para CSVs do Jira
"""

import logging
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from ..models.ticket import Ticket
from .csv_parser import ler_csv

logger = logging.getLogger(__name__)


# Mapeamento de nomes de colunas do Jira para os campos esperados
JIRA_COLUMN_MAP = {
    'Tipo de item': 'tipologia',
    'Responsável': 'responsavel',
    'Relator': 'relator',
    'Componentes': 'componente',
    'Prioridade': 'prioridade',
    'Status': 'status',
    'Criado': 'data_abertura',
    'Atualizado(a)': 'data_fechamento',
    'Servidores / Cluster': 'servidor'
}

# Mapeamento de tipologias
TIPOLOGIA_MAP = {
    'Support': 'Support',
    'Tarefa': 'Task',
    'Incidente': 'Incident',
    'Bug': 'Bug'
}

# Mapeamento de componentes para origem
COMPONENTE_ORIGEM_MAP = {
    'Database': 'Database',
    'Middleware': 'Middleware',
    'Infraestruturas': 'Infraestrutura',
    'Portal': 'Middleware',
    'PSRM': 'Middleware',
    'Batch Server': 'Middleware',
    'Jira Server': 'Infraestrutura',
    'AD/BI': 'AD/BI'
}


def converter_data(data_str: str) -> datetime:
    """
    Converte string de data do Jira para datetime
    
    Args:
        data_str: String no formato "DD/MM/YYYY HH:MM"
        
    Returns:
        datetime object
    """
    try:
        return datetime.strptime(data_str.strip(), "%d/%m/%Y %H:%M")
    except ValueError:
        logger.warning(f"Não foi possível converter data: {data_str}")
        return datetime.now()


def mapear_tipologia(tipo_jira: str) -> str:
    """Mapeia tipo do Jira para tipologia padrão"""
    return TIPOLOGIA_MAP.get(tipo_jira, tipo_jira)


def obter_origem(componente: str) -> str:
    """Obtém a origem baseado no componente"""
    return COMPONENTE_ORIGEM_MAP.get(componente, componente)


def parser_jira_csv(caminho: Path) -> List[Ticket]:
    """
    Parser específico para CSV do Jira
    
    Args:
        caminho: Caminho do arquivo CSV do Jira
        
    Returns:
        Lista de objetos Ticket
    """
    try:
        # Ler CSV com delimitador de ponto e vírgula
        # Tentar diferentes encodings
        dados_brutos = []
        encodings = ['latin1', 'utf-8', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(caminho, 'r', encoding=encoding) as f:
                    import csv
                    reader = csv.DictReader(f, delimiter=';')
                    dados_brutos = list(reader)
                logger.info(f"CSV lido com sucesso usando encoding: {encoding}")
                break
            except UnicodeDecodeError:
                continue
        
        if not dados_brutos:
            raise ValueError("Não foi possível ler o arquivo com nenhum dos encodings suportados")
        
        logger.info(f"Lidos {len(dados_brutos)} registros do Jira CSV")
        
        tickets = []
        
        for idx, linha in enumerate(dados_brutos, 1):
            try:
                # Extrair dados
                tipo_jira = linha.get('Tipo de item', '').strip()
                componente = linha.get('Componentes', '').strip()
                status = linha.get('Status', '').strip()
                data_abertura_str = linha.get('Criado', '').strip()
                data_atualizacao_str = linha.get('Atualizado(a)', '').strip()
                
                # Mapear valores
                tipologia = mapear_tipologia(tipo_jira)
                origem = obter_origem(componente)
                data_abertura = converter_data(data_abertura_str)
                data_fechamento = converter_data(data_atualizacao_str) if status.lower() == 'fechada' else None
                
                # Criar ID único
                ticket_id = f"JIRA-{data_abertura.strftime('%Y%m%d')}-{idx:04d}"
                
                # Criar ticket
                ticket = Ticket(
                    ticket_id=ticket_id,
                    titulo=f"{tipo_jira} - {componente}",
                    descricao=f"{componente} - {status}",
                    tipologia=tipologia,
                    origem=origem,
                    componente=componente,
                    servidor=linha.get('Servidores / Cluster', '').strip(),
                    status=status,
                    data_abertura=data_abertura,
                    data_fechamento=data_fechamento,
                    responsavel=linha.get('Responsável', '').strip(),
                    relator=linha.get('Relator', '').strip(),
                    prioridade=linha.get('Prioridade', '').strip()
                )
                
                tickets.append(ticket)
            
            except Exception as e:
                logger.error(f"Erro ao processar linha {idx}: {e}")
                continue
        
        logger.info(f"Convertidos {len(tickets)} tickets com sucesso")
        return tickets
    
    except Exception as e:
        logger.error(f"Erro ao fazer parser do Jira CSV: {e}")
        raise
