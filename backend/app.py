from flask import Flask, jsonify, request
import time
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import sqlalchemy

# Load environment variables
load_dotenv()

db_config = {
    "pool_size": 5,
    "max_overflow": 2,
    "pool_timeout": 30,  # seconds
    "pool_recycle": 1800,  # seconds
}

def init_unix_connection_engine():
    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+pg8000",
            username=os.environ.get("POSTGRES_USER"),
            password=os.environ.get("POSTGRES_PASSWORD"),
            database=os.environ.get("POSTGRES_DB"),
            query={
                "unix_sock": f"/cloudsql/{os.environ.get('CLOUD_SQL_CONNECTION_NAME')}/.s.PGSQL.5432"
            },
        ),
        **db_config
    )
    pool.dialect.description_encoding = None
    return pool

# Initialize database connection
db = init_unix_connection_engine()

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
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
