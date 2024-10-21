import threading
import time
from redis import Redis
from crud import get_pedido_by_id_query, update_logic
from models import PedidoDB

redis = Redis(host="redis", port=6379, decode_responses=True) 

stream_order_completed = 'order_completed'
stream_order_refund = 'order_refund'
group = 'payment_group'
                
def start():
    crea_grupo()
    start_consumer()
      
        
def crea_grupo():
    try:
        redis.xgroup_create(stream_order_refund, group, mkstream=True)
        print (f"Consumer group {group} in stream {stream_order_refund} created", flush=True)     
    except Exception as ex:
        print(f"Excepción creando grupo: {ex}", flush=True)        


class BackgroundTaskCheckRefund(threading.Thread):
    '''
    Consulta stream Redis key cada 5 segundos por eventos de refunds y actualiza el estado del pedido
    '''
    def run(self,*args,**kwargs):
        while True:
            try:        
                results = redis.xreadgroup(group, stream_order_refund, {stream_order_refund: '>'}, None)
                if results != []:
                    print(f"results {results}", flush=True)
                    for result in results:
                        obj = result[1][0][1]
                        try:
                            print(f"Se recibe evento de obj {obj}", flush=True)
                            id = obj['id']
                            query_pedido_by_id = get_pedido_by_id_query(id)
                            nuevo_pedido: PedidoDB = query_pedido_by_id.first()        
                            nuevo_pedido.status = 'refunded'                            
                            pedido_dict = nuevo_pedido.to_dict()
                            print(f"pedido updated {pedido_dict}", flush=True)
                            updated = update_logic(query_pedido_by_id, pedido_dict)                                                                         
                            print(f"pedido {id} updated {updated}", flush=True)
                        except Exception as ex:
                            print(f"Excepción actualizando pedido ex {ex}", flush=True)                            
                else:
                    print(f"REDIS: No new events in {group}:{stream_order_refund}", flush=True)            
            except Exception as e:
                print(f"REDIS: Excepción consultando nuevos eventos ex:  {str(e)}", flush=True)    
            time.sleep(5)
            
            
def start_consumer():
    try:
        t = BackgroundTaskCheckRefund()
        t.start()
        print ("BackgroundTaskCheckRefund started", flush=True) 
    except Exception as ex:
        print(f"Excepción start_consumer: {ex}", flush=True)      