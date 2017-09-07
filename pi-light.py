#!/usr/bin/env python
import os
import time
import ADC0832
import redis
import boto3
import pygame
from pygame import mixer

#Set AWS details from enviroment varibles
#test = os.environ['MAIL']
#print test
aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY'],
region = os.environ['AWS_DEFAULT_REGION'],
region_name = os.environ['AWS_DEFAULT_REGION'],

#open file with redis details
f = open('../redis.txt')
redis_info = f.readlines()
f.close()

#Split the file
redis_details = []
for line in redis_info:
    redis_details = line.split(',')
    #use redis details from file to login to redis instance on PCF
    r = redis.Redis(host=redis_details[0], port=redis_details[1], password=redis_details[2])
    

def init():
    ADC0832.setup()

def loop():
    count = 0
    #loop to gather brightness value and populate varible
    while count < 2:
        brightness = ADC0832.getResult() - 80
        if brightness < 0:
            brightness = 0
        if brightness > 100:
            brightness = 100
        #write brightness varible to redis
        r.set('bdata', brightness)
        #output brightness value to console, not needed for app but helpful for testing
        print brightness

        time.sleep(1.0)
        count += 1

    #I'm just going to get brightness read via AWS Polly once at the end of the loop
    #as I don't have my sensor board with my Pi
    polly = boto3.client('polly')
    words_to_say = "The current brightness is" + 'brightness' + ",and ,Polly would like a cracker"

    response = polly.synthesize_speech(
        OutputFormat='ogg_vorbis',
        Text=words_to_say,
        TextType='text',
        VoiceId='Emma')    
    with open('speech.oga', 'wb') as s:
        s.write(response['AudioStream'].read())        
    mixer.init()
    mixer.music.load('speech.oga')
    mixer.music.play()


        

if __name__ == '__main__':
    init()
    try:
        loop()
    except KeyboardInterrupt: 
        ADC0832.destroy()
        print 'The end !'