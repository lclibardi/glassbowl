from flask import Flask, render_template, request
from query_tools import *
from query_api import *
import logging,sys
from peer_puller import *


app = Flask(__name__,  template_folder='client', static_folder='client/static')
import json
app.config['FLASK_LOG_LEVEL'] = 'DEBUG'
logging.basicConfig(stream=sys.stderr)
app.logger.addHandler(logging.StreamHandler(stream=sys.stderr))

# mysql = MySQL()

# MySQL configurations
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = ''
# app.config['MYSQL_DATABASE_DB'] = 'glass'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    data = request.data
    try:
        data = json.loads(data)
    except:
        return json.dumps({'status': "error"})
    url = data.get('url')
    if url:
        clean_url = url.strip()
        if clean_url.startswith("http:"):
            clean_url = "https:" + clean_url[5:]
        r = search_query(clean_url)
        return json.dumps(r)
    else:
        return json.dumps({'status': "error"})
    
LI_ACCESS_URL = "https://www.linkedin.com/uas/oauth2/accessToken"

@app.route('/send_text', methods=['GET', 'POST'])
def send_text():
    data = request.data
    try:
        data = json.loads(data)
    except:
        return json.dumps({'status': "error"})
    text = data.get('text')    
    if text:
        r = search_text(text)
        return json.dumps(r)
    else:
        return json.dumps({'status': "error"})

if __name__ == '__main__':
    app.run(threaded=True)
    # app.run(host='0.0.0.0')
