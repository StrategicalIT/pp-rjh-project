#!/usr/bin/env python
import os
import json
import uuid
from flask import Flask
import redis

app = Flask(__name__)
my_uuid = str(uuid.uuid1())
BLUE = "#777799"
GREEN = "#99CC99"

VCAP_SERVICES = json.loads(os.environ['VCAP_SERVICES'])
CREDENTIALS = VCAP_SERVICES["rediscloud"][0]["credentials"]
r = redis.Redis(host=CREDENTIALS["hostname"], port=CREDENTIALS["port"], password=CREDENTIALS["password"])
bright = r.get('bdata')

@app.route('/')
def mainmenu():

    return """
    <html>
    <body>
    
    <center><h1>The brightness at your location is:<br/>
    {}</br>
    </center>
    </body>
    </html>
    """.format(bright)

   
if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
