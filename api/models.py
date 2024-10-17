from database import Base
from sqlalchemy import Column, Integer, String
            
class FarmacoDB(Base):
    __tablename__ = "farmacos"

    id = Column(Integer,primary_key=True,nullable=False)
    nombre = Column(String,nullable=False)
    tipo = Column(String,nullable=False)    