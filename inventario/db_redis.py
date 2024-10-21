import threading
import time
from redis import Redis
from crud import get_farmaco_by_id_query, update_logic
from models import FarmacoDB
from sqlalchemy.orm import Query

redis = Redis(host="redis", port=6379, decode_responses=True) 

stream_order_completed = 'order_completed'
group = 'inventory_group'
stream_order_refund = 'order_refund'
                
def start():
    crea_grupo()
    start_consumer()
      
        
def crea_grupo():
    try:
        redis.xgroup_create(stream_order_completed, group, mkstream=True)
        print (f"Consumer group {group} in stream {stream_order_completed} created", flush=True)     
    except Exception as ex:
        print(f"Excepción creando grupo: {ex}", flush=True)        


class BackgroundTaskCheckNewOrder(threading.Thread):
    '''
    Consulta stream Redis key cada 5 segundos por eventos de nuevas órdenes y actualiza el inventario del pedido solicitado en Postgres
    '''
    def run(self,*args,**kwargs):
        while True:
            try:        
                results = redis.xreadgroup(group, stream_order_completed, {stream_order_completed: '>'}, None)
                if results != []:                    
                    for result in results:
                        obj = result[1][0][1]
                        try:
                            print(f"se recibe evento de obj {obj}", flush=True)
                            pedido_id = obj['id']
                            id = obj['product_id']
                            farmaco_id_query: Query[FarmacoDB] = get_farmaco_by_id_query(id)
                            nuevo_farmaco: FarmacoDB = farmaco_id_query.first()        
                            cantidad_pedida = int(obj['quantity'])
                            print(f"Evento cambio inventario: pedido {pedido_id} quantity {cantidad_pedida} stock del fármaco {id}: {nuevo_farmaco.quantity}")
                            if nuevo_farmaco.quantity<cantidad_pedida:
                                print(f"No se puede tramitar pedido {pedido_id} fármaco {id} quantity {cantidad_pedida}: No hay stock")
                                refund(obj)
                                return
                            nuevo_farmaco.quantity = nuevo_farmaco.quantity - int(cantidad_pedida)                                                        
                            farmaco_dict = nuevo_farmaco.to_dict()
                            print(f"farmaco updated {farmaco_dict}", flush=True)
                            updated = update_logic(farmaco_id_query, farmaco_dict)                                             
                            print(f"farmaco {id} updated {updated}", flush=True)
                        except Exception as ex:
                            print(f"Excepción actualizando farmaco ex {ex}", flush=True)
                            refund(obj)
                else:
                    print(f"REDIS: No new events in {group}:{stream_order_completed}", flush=True)            
            except Exception as e:
                print(f"REDIS: Excepción consultando nuevos eventos ex:  {str(e)}", flush=True)    
            time.sleep(5)
            
            
def refund(obj):    
    print("Se solicita refund")
    redis.xadd(stream_order_refund, obj, '*')                
    
    
def start_consumer():
    try:
        t = BackgroundTaskCheckNewOrder()
        t.start()
        print ("BackgroundTaskCheckNewEvents started", flush=True) 
    except Exception as ex:
        print(f"Excepción start_consumer: {ex}", flush=True)      