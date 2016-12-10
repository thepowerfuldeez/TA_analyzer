from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def root():
    return render_template('index.html')

app.run(host='0.0.0.0', debug=True)