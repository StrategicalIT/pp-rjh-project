#!/usr/bin/env python
import time
import uuid
import ADC0832
import redis

# app = Flask(__name__)
station_id = str(uuid.uuid1())

r = redis.Redis(host='123.12.148.95', port='15379', password='ABCDEFG1231LQ4L')

def init():
    ADC0832.setup()

def loop():
    while True:
        brightness = ADC0832.getResult() - 80
        if brightness < 0:
    			brightness = 0
        if brightness > 100:
    			brightness = 100

		# print 'brightness = %d' % brightness
		Counter = r.incr('new_counter')
        brightness_data = 'brightness' + str(Counter)
        # print "the name of the new key is: " + brightnessdata

		r.hmset(brightness_data,{'station':station_id,'brightness':brightness})
        time.sleep(0.5)

if __name__ == '__main__':
    init()
    try:
        loop()
    except KeyboardInterrupt: 
        ADC0832.destroy()
        print 'The end !'
