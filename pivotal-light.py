#!/usr/bin/env python
import os
import json
import requests
from flask import Flask
import redis

app = Flask(__name__)

VCAP_SERVICES = json.loads(os.environ['VCAP_SERVICES'])
CREDENTIALS = VCAP_SERVICES["rediscloud"][0]["credentials"]
r = redis.Redis(host=CREDENTIALS["hostname"], port=CREDENTIALS["port"], password=CREDENTIALS["password"])
bright = r.get('bdata')

url = "http://api.wunderground.com/api/459098590d3c97e4/conditions/q/AU/melbourne.json"
response = requests.get(url)
parsed = json.loads(response.content)
weather = parsed["current_observation"]["weather"]
temp = parsed["current_observation"]["temp_c"]
hum = parsed["current_observation"]["relative_humidity"]

@app.route('/')
def mainmenu():

    bright_html = """
    <html>
    <body>
    
    <center><h1>The brightness at your location is:</br>
    {}</br>
    </center>
    </body>
    </html>
    """.format(bright)

    weather_html = """
    <html>
    <body>
    </br>
    <centre><h1>and the weather in Melbourne is: {}</br>
    The temp is: {} degress celsius</br>
    And the humidity is: {}</br>
    </centre>
    </body>
    </html>
    """.format(weather, temp, hum)

    final_html = bright_html + weather_html
    return final_html


   
if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
