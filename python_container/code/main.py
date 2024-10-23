from datetime import datetime
from time import sleep

for i in range(100):
  print(datetime.now(), flush=True)
  sleep(2)
