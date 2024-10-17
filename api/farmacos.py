from fastapi import APIRouter, Depends, HTTPException, Path, status
from schemas import FarmacoNuevo, FarmacoAlmacenado
from models import FarmacoDB
from sqlalchemy.orm import Session
from database import get_db

'''
Métodos HTTP para realizar operaciones CRUD (Create Read Update Delete) sobre un recurso de fármacos con Postgres
'''

tag="farmacos"
router = APIRouter(tags=[tag], prefix=f"/{tag}")

@router.get('/', response_model=list[FarmacoAlmacenado], summary="Obtiene todos los fármacos almacenados")
def get_farmacos(db: Session = Depends(get_db)):
    return db.query(FarmacoDB).all()    


@router.post('/', response_model=FarmacoAlmacenado, status_code=status.HTTP_201_CREATED, summary="Almacena un nuevo fármaco")
def test_posts_sent(nuevo_farmaco:FarmacoNuevo, db:Session = Depends(get_db)):
    farm_almacenado = FarmacoDB(**nuevo_farmaco.model_dump())
    db.add(farm_almacenado)
    db.commit()
    db.refresh(farm_almacenado)
    return farm_almacenado


@router.get('/{id}', response_model=FarmacoAlmacenado, status_code=status.HTTP_200_OK, summary="Obtiene un fármaco a partir de su identificador")
def get_test_one_post(id:int = Path(..., gt=0, description="Identificador del fármaco", example="1"), db:Session = Depends(get_db)):
    return get_farmaco(id, db).first()        


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, summary="Elimina un fármaco")
def delete_test_post(id:int = Path(..., gt=0, description="Identificador del fármaco", example="1"), db:Session = Depends(get_db)):
    farm = get_farmaco(id, db)            
    farm.delete(synchronize_session=False)
    db.commit()


@router.put('/{id}', response_model=FarmacoAlmacenado, summary="Actualiza un fármaco")
def update_test_post(updated_farm:FarmacoNuevo, id:int = Path(..., gt=0, description="Identificador del fármaco", example="1"), db:Session = Depends(get_db)):
    farm = get_farmaco(id, db)            
    farm.update(updated_farm.model_dump(), synchronize_session=False)
    db.commit()
    return farm.first()


def get_farmaco(id: int, db: Session):    
    farm = db.query(FarmacoDB).filter(FarmacoDB.id == id)
    if farm.first() is None:
        raise HTTPException(status_code=404, detail=f"Fármaco {id} no encontrado")
    return farm

