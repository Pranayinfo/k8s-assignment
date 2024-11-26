from flask import Flask, jsonify, request
import time
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
import os

# Load environment variables
load_dotenv()

db_name = os.environ.get('POSTGRES_DB')
db_user = os.environ.get('POSTGRES_USER')
db_pass = os.environ.get('POSTGRES_PASSWORD')
db_host = os.environ.get('POSTGRES_HOST')
db_port = os.environ.get('POSTGRES_PORT')
port = os.environ.get('PORT', 9000)  # Get the port from environment variable or default to 9000

db_string = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
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

def wait_for_db():
    retries = 10
    while retries > 0:
        try:
            # Attempt to connect to the database
            with Session(db) as session:
                session.execute("SELECT 1")
            print("Database is ready!")
            break
        except Exception as e:
            print(f"Database not ready, retrying: {e}")
            time.sleep(5)
            retries -= 1
            if retries == 0:
                raise Exception("Database is not ready after multiple attempts.")

if __name__ == '__main__':
    wait_for_db()  # Wait until the DB is ready
    db_init()  # Initialize the database schema
    app.run(host='0.0.0.0', port=int(port), debug=True)  # Bind to the correct port
