from typing import Any, Generator
from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# Postgres
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres_ped/{POSTGRES_DB}"

# SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def start():        
    Base.metadata.create_all(bind=engine)
    print("PostgresDB Pedidos created", flush=True)


def get_db() -> Generator[Session, Any, None]:
    db = SessionLocal()
    try:        
        yield db
    finally:
        db.close()        

    
