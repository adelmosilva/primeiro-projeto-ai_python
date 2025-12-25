"""
Configuração de banco de dados com SQLAlchemy
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv

load_dotenv()

# Obter URL do banco de dados
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:postgres@localhost:5432/tickets_db'
)

# Configurar engine com pool de conexões
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    echo=False,  # Mude para True para debug SQL
    pool_pre_ping=True,  # Testar conexão antes de usar
    connect_args={
        "connect_timeout": 10,
        "application_name": "tickets_app"
    }
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)


def get_db() -> Session:
    """Dependency para obter sessão do banco"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Inicializar tabelas do banco de dados"""
    from backend.models import Base
    Base.metadata.create_all(bind=engine)
    print("✅ Banco de dados inicializado!")


def test_connection():
    """Testar conexão com banco de dados"""
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            print("✅ Conexão com PostgreSQL estabelecida!")
            return True
    except Exception as e:
        print(f"❌ Erro ao conectar ao PostgreSQL: {e}")
        return False
