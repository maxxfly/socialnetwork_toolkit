import time
import progressbar
import random

time_to_sleep = random.randint( 5*60, 45*60 ) 

for i in progressbar.progressbar(range(time_to_sleep)):
    time.sleep(1)
