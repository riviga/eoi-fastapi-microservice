from fastapi import HTTPException, status
import requests
from db_mongodb import pedidos_collection, mapper_pedido
from schemas import PedidoAlmacenado, PedidoAlmacenar, PedidoNuevo
from bson.objectid import ObjectId


'''
Operaciones CRUD sobre MongoDB
'''


def get_all():
    students: list[PedidoAlmacenado] = []
    for pedido in pedidos_collection.find():
        students.append(mapper_pedido(pedido))
    return students    


def get_by_id(id: int):
    pedido = pedidos_collection.find_one({"_id": ObjectId(id)})
    if pedido:
        return mapper_pedido(pedido)    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pedido {id} no encontrado")    


def save(pedido_nuevo: PedidoNuevo):        
    print(f"save pedido_nuevo {pedido_nuevo}")
    url_get_farmaco = f"http://inventario:8000/farmacos/{pedido_nuevo.product_id}"
    req = requests.get(url_get_farmaco)
    farmaco = req.json()
    print(f"Respuesta url_get_farmaco [{url_get_farmaco}] = {farmaco}")
    
    if pedido_nuevo.quantity>farmaco["quantity"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No hay tanto stock del fármaco {pedido_nuevo.product_id}")    
    
    pedido_almacenar = PedidoAlmacenar(
        product_id=pedido_nuevo.product_id,
        quantity=pedido_nuevo.quantity,
        price=farmaco['price'],
        fee=farmaco['price'] * 0.2,
        total=farmaco['price'] * 1.2,        
        status='pending')
    print(f"pedido_almacenar {pedido_almacenar}", flush=True)
    pedido_almacenado = pedidos_collection.insert_one(pedido_almacenar.model_dump())
    nuevo_pedido = pedidos_collection.find_one({"_id": pedido_almacenado.inserted_id})
    print(f"pedido_almacenado {nuevo_pedido}")
    return mapper_pedido(nuevo_pedido)

    
def update_state(id: str, state: str):
    pedido = get_by_id(id)
    pedido.status = state
    update(id, pedido)    
    
    
def update(id, pedido: PedidoAlmacenado) :
    print(f"pedido a actualizar {pedido}", flush=True)    
    pedido_dict = {k: v for k, v in pedido.model_dump().items() if v is not None}
    updated_pedido = pedidos_collection.update_one({"_id": ObjectId(id)}, {"$set": pedido_dict})
    if not updated_pedido:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"There was an error updating the order {id}")
    print(f"Pedido with id {id} updated", flush=True)   
    
    
def delete(id) :        
    delete_count = pedidos_collection.delete_many({"_id": ObjectId(id)})
    if delete_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pedido {id} no encontrado")    
    print(f"Pedido with id {id} updated", flush=True)   
    
    
def delete_all() :        
    delete_count = pedidos_collection.delete_many({})
    print(f"Se han borrado {delete_count.deleted_count} pedidos", flush=True)   