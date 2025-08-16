from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Função para criar as tabelas no banco (main.py)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.create_all(bind=engine)

def create_db_and_tables() -> None:
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")