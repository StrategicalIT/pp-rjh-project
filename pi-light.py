#!/usr/bin/env python
import time
import uuid
import ADC0832
import redis

# app = Flask(__name__)
station_id = str(uuid.uuid1())

r = redis.Redis(host='redis-18169.c14.us-east-1-2.ec2.cloud.redislabs.com', port='18169', password='9qQFLXoHPjBTPbtn')

def init():
    ADC0832.setup()

def loop():
    count = 0
    while count < 100:
        brightness = ADC0832.getResult() - 80
        if brightness < 0:
    			brightness = 0
        if brightness > 100:
    			brightness = 100

		counter = r.incr('new_counter')
		brightness_data = 'brightness' + str(counter)
		r.hmset(brightness_data,{'station':station_id,'brightness':brightness})
		time.sleep(0.5)

if __name__ == '__main__':
    init()
    try:
        loop()
    except KeyboardInterrupt: 
        ADC0832.destroy()
        print 'The end !'