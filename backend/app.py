from flask import *
import time
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

load_dotenv()

db_name = os.environ.get('POSTGRES_DB')
db_user = os.environ.get('POSTGRES_USER')
db_pass = os.environ.get('POSTGRES_PASSWORD')
db_host = os.environ.get('POSTGRES_HOST')
db_port = os.environ.get('POSTGRES_PORT')

db_string = 'postgresql://{}:{}@{}:{}/{}'.format(
    db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)

app = Flask(__name__)


@app.route('/ping')
def ping_pong():

    return jsonify({"ping": "Altair"})


@app.route('/update', methods=['POST', 'GET'])
def start():

    if request.method == 'POST':
        name = request.values.get("name")
        info = request.values.get("info")
        comments = request.values.get("comments")

        name = "{" + name + "}"
        info = "{" + info + "}"
        comments = "{" + comments + "}"

        query = f"insert into users values ('{str(name)}','{str(info)}','{str(comments)}')"
        db.execute(query)

        return jsonify("Entry Added")

    return jsonify({"Message": "Please send data"})


@app.route('/view', methods=['POST', 'GET'])
def view():

    query = f"select * from users"

    data = db.execute(query)

    results = data.fetchall()

    result_dict = {
        "data": []
    }

    for result in results:
        result_dict['data'].append(list(result))

    print(result_dict, results)

    return jsonify(result_dict)


def db_init():

    query = f"create table IF NOT EXISTS users ( name varchar(1000),info varchar(1000),comments varchar(1000) )"

    db.execute(query)


if __name__ == '__main__':
    time.sleep(15)
    db_init()
    app.run(host='0.0.0.0', port=9000, debug=True)
