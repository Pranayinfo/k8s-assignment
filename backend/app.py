from flask import Flask, jsonify, request
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
import os
import time

# Load environment variables
load_dotenv()

# Database credentials from environment variables
db_name = os.environ.get('POSTGRES_DB')
db_user = os.environ.get('POSTGRES_USER')
db_pass = os.environ.get('POSTGRES_PASSWORD')
cloud_sql_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

# Use Unix socket for Cloud SQL connection
db_string = f"postgresql://{db_user}:{db_pass}@/cloudsql/{cloud_sql_connection_name}/{db_name}"
db = create_engine(db_string)

app = Flask(__name__)

@app.route('/ping')
def ping_pong():
    return jsonify({"ping": "Altair"})

@app.route('/update', methods=['POST'])
def start():
    name = request.values.get("name")
    info = request.values.get("info")
    comments = request.values.get("comments")

    if not (name and info and comments):
        return jsonify({"Message": "Invalid data"}), 400

    query = text("INSERT INTO users (name, info, comments) VALUES (:name, :info, :comments)")
    with Session(db) as session:
        session.execute(query, {"name": name, "info": info, "comments": comments})
        session.commit()

    return jsonify("Entry Added")

@app.route('/view', methods=['GET'])
def view():
    query = text("SELECT * FROM users")
    with Session(db) as session:
        results = session.execute(query).fetchall()

    result_dict = {"data": [dict(row) for row in results]}
    return jsonify(result_dict)

def db_init():
    query = text("""
        CREATE TABLE IF NOT EXISTS users (
            name VARCHAR(1000),
            info VARCHAR(1000),
            comments VARCHAR(1000)
        )
    """)
    with Session(db) as session:
        session.execute(query)
        session.commit()

if __name__ == '__main__':
    time.sleep(15)  # Wait for the database to be ready
    db_init()
    app.run(host='0.0.0.0', port=9000, debug=True)
