from pymongo import MongoClient
from schemas import PedidoAlmacenado

MONGO_DETAILS = "mongodb://mongo:27017"

client = MongoClient(MONGO_DETAILS)

database = client.pedidos
pedidos_collection = database.get_collection("pedidos_collection")


print("MongoDB started", flush=True)

def mapper_pedido(pedido) -> PedidoAlmacenado:
    dict = {
        "id": str(pedido["_id"]),
        "product_id": pedido["product_id"],
        "price": pedido["price"],
        "fee": pedido["fee"],
        "total": pedido["total"],
        "quantity": pedido["quantity"],
        "status": pedido["status"]
    }
    return PedidoAlmacenado(**dict)