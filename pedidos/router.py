from fastapi import APIRouter, Path, status
from schemas import PedidoNuevo, PedidoAlmacenado
import crud
from db_redis import redis, stream_order_pending

'''
Métodos HTTP para realizar operaciones CRUD (Create Read Update Delete) sobre pedidos
'''

tag="pedidos"
router = APIRouter(tags=[tag], prefix=f"/{tag}")

@router.get('', response_model=list[PedidoAlmacenado], summary="Obtiene todos los pedidos almacenados")
def get_all():
    return crud.get_all()    


@router.delete('', status_code=status.HTTP_204_NO_CONTENT, summary="Borra todos los pedidos")
def delete():
    return crud.delete_all()    


@router.post('', response_model=PedidoAlmacenado, status_code=status.HTTP_201_CREATED, summary="Almacena un nuevo pedido")
def post(nuevo_pedido:PedidoNuevo):    
    pedido_nuevo = crud.save(nuevo_pedido)  # state = pending    
    response = redis.xadd(stream_order_pending, pedido_nuevo.model_dump(), '*')
    print(f"Evento pedido id {pedido_nuevo.id} enviado a Redis {stream_order_pending} response {response}")
    return pedido_nuevo
        
        
@router.get('/{id}', response_model=PedidoAlmacenado, status_code=status.HTTP_200_OK, summary="Obtiene un pedido a partir de su identificador")
def get_id(id:str = Path(..., min_length=1, description="Identificador del pedido", example="6717ae3823703a2307039bfa")):
    return crud.get_by_id(id)    


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, summary="Borra un pedido")
def delete(id:str = Path(..., min_length=1, description="Identificador del pedido", example="6717ae3823703a2307039bfa")):
    return crud.delete(id)    