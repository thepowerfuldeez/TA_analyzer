from flask import *
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def root():
    resp = make_response(render_template('index.html'))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

app.run(host='0.0.0.0', debug=True)