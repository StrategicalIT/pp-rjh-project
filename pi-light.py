#!/usr/bin/env python
import time
import uuid
import ADC0832
import redis

# app = Flask(__name__)
station_id = str(uuid.uuid1())

r = redis.Redis(host='host', port='port', password='password')

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

		# counter = r.incr('new_counter')
		# brightness_data = 'brightness' + str(counter)
		# r.hmset('brightness_data',{'station':station_id,'brightness':brightness})
        r.set('bdata',brightness)
        print brightness
        time.sleep(1.0)
        count += 1
        

if __name__ == '__main__':
    init()
    try:
        loop()
    except KeyboardInterrupt: 
        ADC0832.destroy()
        print 'The end !'