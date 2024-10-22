from fastapi import HTTPException
from db_postgres import get_db
from sqlalchemy.orm import Session, Query
from models import FarmacoDB


'''
Operaciones CRUD sobre Postgres
'''


db: Session = next(get_db())

def get_all():
    return db.query(FarmacoDB).all()    


def get_by_id(id: int):
    return get_farmaco_by_id_query(id).first()        


def get_farmaco_by_id_query(id: int):    
    farmaco_id_query = db.query(FarmacoDB).filter(FarmacoDB.id == id)
    if farmaco_id_query.first() is None:
        raise HTTPException(status_code=404, detail=f"Fármaco {id} no encontrado")
    return farmaco_id_query


def save(dic: dict):
    farmaco_nuevo = FarmacoDB(**dic)
    db.add(farmaco_nuevo)
    db.commit()
    db.refresh(farmaco_nuevo)
    return farmaco_nuevo  


def delete(id: int):
    farmaco_id_query = get_farmaco_by_id_query(id)            
    farmaco_id_query.delete(synchronize_session=False)
    db.commit()
    
    
def update(id: int, farmaco_dict: dict):
    farmaco_id_query = get_farmaco_by_id_query(id)            
    return update_logic(farmaco_id_query, farmaco_dict)    


def update_logic(farmaco_id_query: Query[FarmacoDB], farmaco_nuevo:dict):             
    farmaco_id_query.update(farmaco_nuevo, synchronize_session=False)
    db.commit()
    return farmaco_nuevo

