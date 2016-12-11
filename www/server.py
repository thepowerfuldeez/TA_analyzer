from flask import *
import requests

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def root():
    resp = make_response(render_template('index.html'))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/analytics', methods=['POST', 'GET'])
def analytics():
	_id = request.args['id']
	r = requests.get("https://api.vk.com/method/groups.getById?group_id=" + _id + "&fields=photo_100,description")
	
	# хардкод
	resp = r.text[:len(r.text)-1] + ', "sexes": {"men": 30, "women": 30, "undefined": 10} }'
	print(resp)
	return resp

app.run(host='0.0.0.0', debug=True)