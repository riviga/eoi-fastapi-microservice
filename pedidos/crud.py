import requests
from fastapi import HTTPException
from db_postgres import get_db
from sqlalchemy.orm import Session, Query
from models import PedidoDB


'''
Operaciones CRUD sobre Postgres
'''


db: Session = next(get_db())

def get_all():
    return db.query(PedidoDB).all()    


def get_by_id(id: int):
    return get_farmaco_by_id_query(id).first()        


def get_farmaco_by_id_query(id: int):    
    farmaco_id_query = db.query(PedidoDB).filter(PedidoDB.id == id)
    if farmaco_id_query.first() is None:
        raise HTTPException(status_code=404, detail=f"Fármaco {id} no encontrado")
    return farmaco_id_query


def save(pedido_dict: dict):
    product_id = pedido_dict["product_id"]
    url_get_farmaco = f"http://inventario:8000/farmacos/{product_id}"
    req = requests.get(url_get_farmaco)
    product = req.json()
    print(f"Respuesta url_get_farmaco [{url_get_farmaco}] = {product}")
    
    pedido_db = PedidoDB(
        product_id=product_id,
        price=product['price'],
        fee=product['price'] * 0.2,
        total=product['price'] * 1.2,
        quantity=pedido_dict["quantity"],
        status='pending'
    )
        
    db.add(pedido_db)
    db.commit()
    db.refresh(pedido_db)    
    return pedido_db


def delete(id: int):
    farmaco_id_query = get_farmaco_by_id_query(id)            
    farmaco_id_query.delete(synchronize_session=False)
    db.commit()
    
    
def update(id: int, farmaco_nuevo: dict):
    farmaco_id_query = get_farmaco_by_id_query(id)            
    return update_logic(farmaco_id_query, farmaco_nuevo)    


def update_logic(pedido_id_query: Query[PedidoDB], pedido_nuevo:dict):         
    print(f"update pedido_nuevo {pedido_nuevo}")    
    pedido_id_query.update(pedido_nuevo, synchronize_session=False)
    db.commit()
    return pedido_nuevo
