#!/usr/bin/env python
import os
import ADC0832
import redis

f = open('../redis.txt')
redis_info = f.readlines()
f.close()
redis_details = redis_info.split(',')

r = redis.Redis(host=redis_details[1], port=redis_details[2], password=redis_details[3])


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