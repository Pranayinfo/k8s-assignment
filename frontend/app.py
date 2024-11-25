from flask import Flask, render_template,request,jsonify
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

URL = os.environ['BACKEND_URL']

app = Flask(__name__)

@app.route('/ping')
def ping_pong():

    return jsonify({"ping":"Altair"})


@app.route('/',methods = ['POST','GET'])
def start():

    if request.method == 'POST':

        name = request.values.get("name")
        info = request.values.get("info")
        comments = request.values.get("comments")

        data_dict = {
            "name"      :name,
            "info"      :info,
            "comments"  :comments
        }

        r = requests.post(URL + '/update', data = data_dict)

        data = json.loads(r.content)

        message = data

        return render_template('index.html', message=message)

    return render_template('index.html')

@app.route('/view',methods = ['POST','GET'])
def view():

    r = requests.post(URL + '/view')

    data = json.loads(r.content)

    return render_template('view.html', data = data)


if __name__ == '__main__':
    print("please")
    app.run(host = '0.0.0.0', port = 8080, debug = True)
