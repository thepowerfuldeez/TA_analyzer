from flask import *
import requests
from Analyzer import Analyzer

an = Analyzer()

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
	info = an.get_info(_id)
	print(info[0])
	resp = r.text[:len(r.text)-1] + \
	', "sexes": {"men": 30, "women": 30, "undefined": 10}' + \
	', "city": "Либерти-Сити"' + \
	', "school": "МОУ СОШ 13"' + \
	', "university": "МАМИ"' + \
	', "agerange": "14-17"' + \
	', "content": {"music": 50, "photo": 80, "text": 20, "video": 7}' + \
	'}'

	print(resp)
	return resp

app.run(host='0.0.0.0', debug=True)