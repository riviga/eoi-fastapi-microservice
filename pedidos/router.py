import time
from fastapi import APIRouter, BackgroundTasks, Path, status
from db_postgres import get_db
from models import PedidoDB
from schemas import PedidoNuevo, PedidoAlmacenado
from sqlalchemy.orm import Session, Query
import crud
from db_redis import redis

'''
Métodos HTTP para realizar operaciones CRUD (Create Read Update Delete) sobre pedidos
'''

tag="pedidos"
router = APIRouter(tags=[tag], prefix=f"/{tag}")

@router.get('', response_model=list[PedidoAlmacenado], summary="Obtiene todos los pedidos almacenados")
def get_all():
    return crud.get_all()    


@router.post('', response_model=PedidoAlmacenado, status_code=status.HTTP_201_CREATED, summary="Almacena un nuevo pedido")
def post(nuevo_pedido:PedidoNuevo, background_tasks: BackgroundTasks):
    pedido_dict = nuevo_pedido.model_dump()    
    pedido_db = crud.save(pedido_dict)
    pedido_dict["id"] = pedido_db.id
    background_tasks.add_task(order_completed, pedido_dict)
    return pedido_db


def order_completed(pedido_dict: dict):
        db = next(get_db())
        time.sleep(5)
        id = pedido_dict["id"]
        print(f"Pasa periodo de gracia pedido {id}", flush=True)        
        farmaco_id_query = crud.get_farmaco_by_id_query(id)
        pedido_db = farmaco_id_query.first()
        pedido_db.status = 'completed'
        farmaco_id_query.update(pedido_dict, synchronize_session=False)
        db.commit()        
        redis.xadd('order_completed', pedido_dict, '*')
        print(f"Pedido id {pedido_db.id} completado")
        

@router.get('/{id}', response_model=PedidoAlmacenado, status_code=status.HTTP_200_OK, summary="Obtiene un pedido a partir de su identificador")
def get_id(id:int = Path(..., gt=0, description="Identificador del pedido", example="1")):
    return crud.get_by_id(id)    
