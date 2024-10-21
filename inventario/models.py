from db_postgres import Base
from sqlalchemy import Column, Integer, String, Float
            
class FarmacoDB(Base):
    __tablename__ = "farmacos"

    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String,nullable=False)
    price = Column(Float,nullable=False)    
    quantity = Column(Integer,nullable=False)    
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,                        
            "quantity": self.quantity
        }