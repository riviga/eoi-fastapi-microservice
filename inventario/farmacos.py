from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
import sqlalchemy
from schemas import FarmacoNuevo, FarmacoAlmacenado
from models import FarmacoDB
from sqlalchemy.orm import Session, Query
from db_postgres import get_db

'''
Métodos HTTP para realizar operaciones CRUD (Create Read Update Delete) sobre un recurso de fármacos con Postgres
'''

tag="farmacos"
router = APIRouter(tags=[tag], prefix=f"/{tag}")

@router.get('', response_model=list[FarmacoAlmacenado], summary="Obtiene todos los fármacos almacenados")
def get_all(db: Session = Depends(get_db)):
    return db.query(FarmacoDB).all()    


@router.post('', response_model=FarmacoAlmacenado, status_code=status.HTTP_201_CREATED, summary="Almacena un nuevo fármaco")
def post(nuevo_farmaco:FarmacoNuevo, db:Session = Depends(get_db)):
    farmaco_almacenado = FarmacoDB(**nuevo_farmaco.model_dump())
    db.add(farmaco_almacenado)
    db.commit()
    db.refresh(farmaco_almacenado)
    return farmaco_almacenado


@router.get('/{id}', response_model=FarmacoAlmacenado, status_code=status.HTTP_200_OK, summary="Obtiene un fármaco a partir de su identificador")
def get_id(id:int = Path(..., gt=0, description="Identificador del fármaco", example="1"), db:Session = Depends(get_db)):
    return get_farmaco(id, db).first()        


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, summary="Elimina un fármaco")
def delete(id:int = Path(..., gt=0, description="Identificador del fármaco", example="1"), db:Session = Depends(get_db)):
    farmaco = get_farmaco(id, db)            
    farmaco.delete(synchronize_session=False)
    db.commit()


@router.put('/{id}', response_model=FarmacoAlmacenado, summary="Actualiza un fármaco")
def update(farmaco_nuevo:FarmacoNuevo, id:int = Path(..., gt=0, description="Identificador del fármaco", example="1"), db:Session = Depends(get_db)):
    farmaco_db = get_farmaco(id, db)        
    return update_logic(farmaco_db, farmaco_nuevo, db)    


def get_farmaco(id: int, db: Session):    
    farmaco = db.query(FarmacoDB).filter(FarmacoDB.id == id)
    if farmaco.first() is None:
        raise HTTPException(status_code=404, detail=f"Fármaco {id} no encontrado")
    return farmaco


def update_logic(farmaco_db: sqlalchemy.orm.Query, farmaco_nuevo:FarmacoNuevo, db: Session):     
    farmaco_db.update(farmaco_nuevo.model_dump(), synchronize_session=False)
    db.commit()
    return farmaco_db.first()
