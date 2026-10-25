import os
import time

import psycopg2
from flask import Flask

app = Flask(__name__)

DOCTORS = ["dr-anil", "dr-meera", "dr-suresh"]


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        dbname=os.getenv("DB_NAME", "hospital"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )


def init_db():
    # database start aakaan kurachu samayam edukkum, athu vare kaathirikkum
    for _ in range(10):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS tokens (
                    id SERIAL PRIMARY KEY,
                    doctor TEXT NOT NULL,
                    number INT NOT NULL
                )
                """
            )
            conn.commit()
            cur.close()
            conn.close()
            return
        except psycopg2.OperationalError:
            time.sleep(2)
    raise Exception("Could not connect to the database")


init_db()


@app.route("/")
def home():
    return "Hospital Token System"


@app.route("/token/<doctor>/new")
def new_token(doctor):
    if doctor not in DOCTORS:
        return {"error": "Doctor not found"}, 404
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT COALESCE(MAX(number), 0) + 1 FROM tokens WHERE doctor = %s",
        (doctor,),
    )
    number = cur.fetchone()[0]
    cur.execute(
        "INSERT INTO tokens (doctor, number) VALUES (%s, %s)",
        (doctor, number),
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"doctor": doctor, "token": number}


@app.route("/token/<doctor>/list")
def list_tokens(doctor):
    if doctor not in DOCTORS:
        return {"error": "Doctor not found"}, 404
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT number FROM tokens WHERE doctor = %s ORDER BY number",
        (doctor,),
    )
    numbers = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return {"doctor": doctor, "tokens": numbers}


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)