from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine
from databases import Database
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def start():    
    # SQLAlchemy
    Base.metadata.create_all(bind=engine)
    print("PostgresDB created", flush=True)


def get_db():
    db = SessionLocal()
    try:        
        yield db
    finally:
        db.close()        

    
