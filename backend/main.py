from flask import *
from api import api_bp
from flask_cors import CORS
import json
import re


app = Flask(__name__, static_folder='../frontend/dist/static', template_folder='../frontend/dist')
CORS(app)
#  app.register_blueprint(api_bp)

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def index(path):
#     return render_template('index.html')

@app.route('/test', methods=['GET', 'POST'])
def getmethod():
    file_json = '../data/getinfo.json'
    query = request.args.get("query", "")
    # try:
    #     if request.method == 'POST':
    #         return request.form['test']
    #     else:
    #         return request.args.get('test', '')
    # except Exception as e:
    # return render_template('../data/getinfo.json')
    if query != "":
        return query
    else:
        return "error"

@app.route('/test_get', methods=['GET'])
def test_get():
    return jsonify({
        "response": "hello world"
    })

@app.route('/test_post', methods=['POST'])
def test_post():
    data = request.get_json()
    message = data.get('message')
    return jsonify({
        "message": message
    })



if __name__ == '__main__':
    app.run()
