import threading
import time
from redis import Redis
from crud import update_state
import os

redis = Redis(host="redis", port=6379, decode_responses=True) 

stream_order_pending = os.getenv("REDIS_STREAM_PENDING")
stream_order_complete = os.getenv("REDIS_STREAM_COMPLETE")
stream_order_refund = os.getenv("REDIS_STREAM_REFUND")
delay = int(os.getenv("REDIS_DELAY_SECONDS", 5))
group = 'payment_group'
                      

try:
    redis.xgroup_create(stream_order_refund, group, mkstream=True)
    print (f"Consumer group {group} in stream {stream_order_refund} created", flush=True)     
        
    redis.xgroup_create(stream_order_complete, group, mkstream=True)
    print (f"Consumer group {group} in stream {stream_order_complete} created", flush=True)     
except Exception as ex:
    print(f"Excepción creando grupo: {ex}", flush=True)        


def backgroundTaskOrderRefund():
    '''
    Consulta stream Redis key cada 5 segundos por pedidos para refund y actualiza el estado del pedido 
    '''
    while True:
        try:        
            results = redis.xreadgroup(group, "my_consumer", {stream_order_refund: '>'}, count=10)            
            if results != []:          
                print(f"Results {results}", flush=True)        
                eventos = [i for i in results[0][1]]
                print(f"Nuevos eventos {stream_order_refund}: {len(eventos)}", flush=True)      
                for evento in eventos:
                    print(f"Nuevo evento {stream_order_refund}: {evento}", flush=True)                                               
                    message_id = evento[0]                                      
                    redis.xack(stream_order_refund, group, message_id)                                  
                    id = evento[1]['id']
                    print(f"Se recibe evento refund de pedido {id}", flush=True)
                    try:                                                 
                        update_state(id, 'refunded')                                                        
                    except Exception as ex:
                        print(f"Excepción actualizando evento refund ex {ex}", flush=True)                            
            # else:
                # print(f"REDIS: No new events in {group}:{stream_order_refund}", flush=True)            
        except Exception as e:
            print(f"REDIS: Excepción consultando nuevos eventos ex:  {str(e)}", flush=True)    
        time.sleep(delay)
        

def backgroundTaskOrderComplete():
    '''
    Consulta stream Redis key cada 5 segundos por pedidos completados y actualiza el estado del pedido
    '''
    while True:
        try:        
            results = redis.xreadgroup(group, stream_order_complete, {stream_order_complete: '>'}, count=10)
            if results != []:                          
                print(f"Results {results}", flush=True)        
                eventos = [i for i in results[0][1]]
                print(f"Nuevos eventos {stream_order_complete}: {len(eventos)}", flush=True)                                                              
                for evento in eventos:
                    print(f"Nuevo evento {stream_order_complete}: {evento}", flush=True)                                               
                    message_id = evento[0]                                  
                    redis.xack(stream_order_complete, group, message_id)                    
                    id = evento[1]['id']
                    print(f"Se recibe evento complete de pedido {id}", flush=True)
                    try:                                                                             
                        update_state(id, 'completed')                                                        
                    except Exception as ex:
                        print(f"Excepción actualizando evento complete ex {ex}", flush=True)                             
            # else:
            #     print(f"REDIS: No new events in {group}:{stream_order_complete}", flush=True)            
        except Exception as e:
            print(f"REDIS: Excepción consultando nuevos eventos ex:  {str(e)}", flush=True)    
        time.sleep(delay)
    

def start_threads():
    try:    
        t1 = threading.Thread(target=backgroundTaskOrderComplete) 
        t2 = threading.Thread(target=backgroundTaskOrderRefund)        
        t1.start()
        print("backgroundTaskOrderComplete started", flush=True)
        t2.start()          
        print("backgroundTaskOrderRefund started", flush=True)
        print(f"Redis started streams [{stream_order_pending}, {stream_order_complete}, {stream_order_refund}] delay [{delay}]", flush=True)
    except Exception as ex:
        print(f"Excepción arranque hilos consumicion streams: {ex}", flush=True) 
    
    