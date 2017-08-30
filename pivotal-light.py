import os
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

COLOR = GREEN

@app.route('/')
def mainmenu():

    ## Very often the HTML needs to be generated dynamically
    ## but the beginning and end of a HTML is likely to be the same
    ## We can create a beginning, middle and end, and concatenate them

    ## Here we use the triple double-quotes format
    begin_html = """
    <html>
    <head>
    <! the link to your CSS would go here>
    </head>"""

    ## Here we use the straight string format
    end_html = "</body></html>"

    ## NOTE:  Triple quotes format is easier when the HTML code requires
    ## quotes itself, ex <img src="myphoto.jpg">
    ## If you want to use the straight string format you can scape them with \
    ## my_html = "<img src=\"myphoto.jpg\">"
    
    ## If a page is completely static you can also render it like this
    ## resp = make_response(render_template('my_static_page.html'))
	## or put the rendr_template function directly in the "return" like this:
	## return render_template('my_static_page.html')
    ## IMPORTANT: The html file must reside in a subdirectory named "templates"

    mid_html =  """
    <body bgcolor="{}">

    <center><h1><font color="white">Hi, I'm GUID:<br/>
    {}</br>
    <u>Main Menu</u>
    </center>
    """.format(COLOR,my_uuid,)

    response = begin_html + mid_html + end_html

    return response

if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
