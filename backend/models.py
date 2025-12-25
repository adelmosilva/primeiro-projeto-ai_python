"""
Modelos SQLAlchemy para sistema de tickets
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Ticket(Base):
    """Modelo para tickets/itens"""
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, index=True)
    
    # Campos do CSV
    tipo_item = Column(String(100), nullable=False, index=True)  # Tipo de item Responsável
    responsavel = Column(String(255), nullable=True, index=True)
    relator = Column(String(255), nullable=True, index=True)  # Origem
    componente = Column(String(255), nullable=False, index=True)  # Módulo
    prioridade = Column(String(50), nullable=True, index=True)
    status = Column(String(50), nullable=False, index=True)
    data_criacao = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    data_atualizacao = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    servidor_cluster = Column(String(255), nullable=False, index=True)
    
    # Rastreamento
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    snapshot_id = Column(Integer, ForeignKey('snapshots.id'), nullable=True)
    
    # Relacionamentos
    snapshot = relationship("Snapshot", back_populates="tickets")

    def __repr__(self):
        return f"<Ticket(id={self.id}, tipo={self.tipo_item}, componente={self.componente})>"


class Snapshot(Base):
    """Modelo para snapshots mensais dos dados"""
    __tablename__ = 'snapshots'

    id = Column(Integer, primary_key=True, index=True)
    
    # Data do snapshot
    mes = Column(Integer, nullable=False)  # 1-12
    ano = Column(Integer, nullable=False)  # YYYY
    data_snapshot = Column(Date, nullable=False, index=True, unique=True)
    
    # Contadores
    total_tickets_abertos = Column(Integer, default=0)
    total_tickets_fechados = Column(Integer, default=0)
    total_geral = Column(Integer, default=0)
    
    # Rastreamento
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    tickets = relationship("Ticket", back_populates="snapshot", cascade="all, delete-orphan")
    analises = relationship("Analise", back_populates="snapshot", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Snapshot(mes={self.mes}, ano={self.ano}, total={self.total_geral})>"


class Analise(Base):
    """Modelo para armazenar análises pré-calculadas"""
    __tablename__ = 'analises'

    id = Column(Integer, primary_key=True, index=True)
    
    # Referência
    snapshot_id = Column(Integer, ForeignKey('snapshots.id'), nullable=False)
    tipo_analise = Column(String(50), nullable=False, index=True)  # 'tipologia', 'top_modulos', 'top_servidores', 'origem'
    
    # Dados da análise (JSON armazenado como texto)
    dados = Column(Text, nullable=False)  # JSON stringified
    
    # Estatísticas
    total_registros = Column(Integer, default=0)
    total_abertos = Column(Integer, default=0)
    total_fechados = Column(Integer, default=0)
    
    # Rastreamento
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    snapshot = relationship("Snapshot", back_populates="analises")

    def __repr__(self):
        return f"<Analise(tipo={self.tipo_analise}, snapshot_id={self.snapshot_id})>"


class ConfiguracaoPeriodo(Base):
    """Modelo para armazenar configurações de período"""
    __tablename__ = 'configuracoes_periodo'

    id = Column(Integer, primary_key=True, index=True)
    
    # Período
    mes_atual = Column(Integer, nullable=False)  # 1-12
    ano_atual = Column(Integer, nullable=False)  # YYYY
    
    # Datas
    data_inicio_ano = Column(DateTime, nullable=False)
    mes_inicio = Column(Integer, default=1)  # Sempre janeiro
    
    # Rastreamento
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<ConfiguracaoPeriodo(mes={self.mes_atual}, ano={self.ano_atual})>"
