#!/usr/bin/env python
import os
import time
import ADC0832
import redis

#open file with redis details
f = open('../redis.txt')
redis_info = f.readlines()
f.close()

#Split the file
redis_details = []
for line in redis_info:
    redis_details = line.split(',')

#use redis details from file to login to redis instance on PCF
r = redis.Redis(host=redis_details[1], port=redis_details[2], password=redis_details[3])


def init():
    ADC0832.setup()

def loop():
    count = 0
    #loop to gather brightness value and populate varible
    while count < 100:
        brightness = ADC0832.getResult() - 80
        if brightness < 0:
            brightness = 0
        if brightness > 100:
            brightness = 100
        #write brightness varible to redis
        r.set('bdata',brightness)
        #output brightness value to console, not need for app but helpful for testing
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