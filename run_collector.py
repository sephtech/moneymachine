import api_collect
import time

i = 0
while True:
    print('~Sekunden: ', i * 10)
    
    api_collect.collect()
    
    time.sleep(10)
    i += 1
