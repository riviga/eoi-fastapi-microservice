import threading
import time
from redis import Redis
from crud import get_farmaco_by_id_query, update_logic
from models import FarmacoDB
from sqlalchemy.orm import Query
import os

redis = Redis(host="redis", port=6379, decode_responses=True) 

stream_order_pending = os.getenv("REDIS_STREAM_PENDING")
stream_order_complete = os.getenv("REDIS_STREAM_COMPLETE")
stream_order_refund = os.getenv("REDIS_STREAM_REFUND")
group = 'inventory_group'     

try:
    redis.xgroup_create(stream_order_pending, group, mkstream=True)
    print (f"Consumer group {group} in stream {stream_order_pending} created", flush=True)     
except Exception as ex:
    print(f"Excepción creando grupo: {ex}", flush=True)        


class BackgroundTaskOrderPending(threading.Thread):
    '''
    Consulta stream Redis key cada 5 segundos por eventos de órdenes pendientes y actualiza el inventario del pedido solicitado en Postgres o no, si no hay stock
    '''
    def run(self,*args,**kwargs):
        while True:
            try:        
                results = redis.xreadgroup(group, "my_consumer", {stream_order_pending: '>'}, count=10)                                
                if results != []:                              
                    print(f"Results {results}", flush=True)        
                    eventos = [i for i in results[0][1]]
                    print(f"Nuevos eventos {stream_order_complete}: {len(eventos)}", flush=True)                                                                                  
                    for evento in eventos:
                        print(f"Nuevo evento {stream_order_pending}: {evento}", flush=True)                                               
                        message_id = evento[0]
                        print(f"Message ID {message_id}", flush=True)                       
                        redis.xack(stream_order_pending, group, message_id)
                        print(f"Message ID {message_id} ACK", flush=True)                       
                        obj = evento[1]
                        try:
                            print(f"Nuevo evento en {stream_order_pending}: {obj}", flush=True)
                            pedido_id = obj['id']
                            id = obj['product_id']
                            farmaco_id_query: Query[FarmacoDB] = get_farmaco_by_id_query(id)
                            nuevo_farmaco: FarmacoDB = farmaco_id_query.first()        
                            cantidad_pedida = int(obj['quantity'])
                            print(f"Evento cambio inventario: pedido {pedido_id} quantity {cantidad_pedida} stock del fármaco {id}: {nuevo_farmaco.quantity}")
                            if nuevo_farmaco.quantity < cantidad_pedida:
                                print(f"No se puede tramitar pedido {pedido_id} fármaco {id} quantity {cantidad_pedida}: No hay stock")
                                refund(obj)
                            else:                                    
                                nuevo_farmaco.quantity = nuevo_farmaco.quantity - int(cantidad_pedida)                                                        
                                farmaco_dict = nuevo_farmaco.to_dict()
                                print(f"farmaco updated {farmaco_dict}", flush=True)
                                updated = update_logic(farmaco_id_query, farmaco_dict)                                                                         
                                print(f"farmaco {id} updated {updated}", flush=True)
                                complete(obj)
                        except Exception as ex:
                            print(f"Excepción tratando order pending farmaco ex {ex}", flush=True)
                            refund(obj)
                # else:
                #     print(f"REDIS: No new events in {group}:{stream_order_pending}", flush=True)            
            except Exception as e:
                print(f"REDIS: Excepción consultando nuevos eventos ex:  {str(e)}", flush=True)    
            time.sleep(5)
            
            
def refund(obj):    
    print(f"Se envía evento refund pedido {obj['id']}", flush=True)
    try:
        redis.xadd(stream_order_refund, obj, '*')       
    except Exception as ex:
        print(f"Excepción envío refund {ex}", flush=True)        
    
    
def complete(obj):    
    print(f"Se envía evento complete pedido {obj['id']}", flush=True)
    try:
        redis.xadd(stream_order_complete, obj, '*')             
    except Exception as ex:
        print(f"Excepción envío complete {ex}", flush=True)
        refund(obj)         
    
    
try:
    t = BackgroundTaskOrderPending()
    t.start()
    print ("BackgroundTaskCheckNewEvents started", flush=True) 
except Exception as ex:
    print(f"Excepción start_consumer: {ex}", flush=True)      
    
def say_hi():
    print(f"Redis started streams {stream_order_pending} {stream_order_complete} {stream_order_refund}", flush=True)
