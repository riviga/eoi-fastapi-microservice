from db_postgres import Base
from sqlalchemy import Column, Integer, String, Float

            
class PedidoDB(Base):
    __tablename__ = "pedidos"

    id = Column(Integer,primary_key=True,nullable=False)
    product_id = Column(Integer,nullable=False)    
    price = Column(Float,nullable=False)    
    fee = Column(Float,nullable=False)    
    total = Column(Float,nullable=False)    
    quantity = Column(Integer,nullable=False)  
    status = Column(String,nullable=False) # pending, completed, refunded   
    
    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "price": self.price,
            "fee": self.fee,
            "total": self.total,
            "quantity": self.quantity,
            "status": self.status
        }