import time
from redis import Redis
from farmacos import get_farmaco, update_logic
from db_postgres import get_db

redis = Redis(host="redis", port=6379, decode_responses=True) 

key = 'order_completed'
group = 'inventory_group'

def start_consumer():
    try:
        redis.xgroup_create(key, group)
        print (f"Consumer group {group} in strem {key} created", flush=True) 
    except Exception as ex:
        print(f"Excepción creando grupo: {ex}", flush=True)
        print ("Group already exists", flush=True)

    while True:
        try:        
            results = redis.xreadgroup(group, key, {key: '>'}, None)
            if results != []:
                db = get_db()
                for result in results:
                    obj = result[1][0][1]
                    try:
                        print(f"se recibe evento de obj {obj}", flush=True)
                        id = obj['product_id']
                        farmaco_db = get_farmaco(id, db)
                        nuevo_farmaco = farmaco_db.first()
                        nuevo_farmaco.quantity = nuevo_farmaco.quantity - int(obj['quantity'])
                        print(f"farmaco updated {nuevo_farmaco}", flush=True)
                        update_logic(farmaco_db, nuevo_farmaco, db)                                             
                        print(f"farmaco {id} updated", flush=True)
                    except Exception as ex:
                        print(f"Excepción actualizando farmaco ex {ex}", flush=True)
                        redis.xadd('order_refund', obj, '*')

        except Exception as e:
            print(f"REDIS: Excepción en bucle obteniendo nuevos eventos ex:  {str(e)}", flush=True)            
        time.sleep(1)