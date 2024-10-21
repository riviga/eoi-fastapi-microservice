from fastapi import APIRouter, Path, status
from schemas import FarmacoNuevo, FarmacoAlmacenado
import crud


'''
Métodos HTTP para realizar operaciones CRUD (Create Read Update Delete) sobre un recurso de fármacos
'''


tag="farmacos"
router = APIRouter(tags=[tag], prefix=f"/{tag}")

@router.get('', response_model=list[FarmacoAlmacenado], summary="Obtiene todos los fármacos almacenados")
def get_all():
    return crud.get_all()


@router.post('', response_model=FarmacoAlmacenado, status_code=status.HTTP_201_CREATED, summary="Almacena un nuevo fármaco")
def post(nuevo_farmaco:FarmacoNuevo):    
    return crud.save(nuevo_farmaco.model_dump())


@router.get('/{id}', response_model=FarmacoAlmacenado, status_code=status.HTTP_200_OK, summary="Obtiene un fármaco a partir de su identificador")
def get_id(id:int = Path(..., gt=0, description="Identificador del fármaco", example="1")):
    return crud.get_by_id(id)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, summary="Elimina un fármaco")
def delete(id:int = Path(..., gt=0, description="Identificador del fármaco", example="1")):
    crud.delete(id)


@router.put('/{id}', response_model=FarmacoAlmacenado, summary="Actualiza un fármaco")
def update(nuevo_farmaco:FarmacoNuevo, id:int = Path(..., gt=0, description="Identificador del fármaco", example="1")):
    farmaco_dict = nuevo_farmaco.model_dump()
    farmaco_dict["id"] = id
    return crud.update(id, farmaco_dict)
