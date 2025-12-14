from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os
import random
from datetime import datetime

app = Flask(__name__, static_folder="frontend")

DB_PATH = "database.db"

SALUDOS = [
    "Hola {name}",
    "¿Qué tal {name}?",
    "ola {name}, ke ase?",
    "Encantado de verte, {name}",
    "Buenaaaas... {name}",
    "Ey {name}, ¿todo bien?",
    "Saludos, {name}",
    "Hola bro, {name}"
]

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS greetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def root():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/greet", methods=["POST"])
def greet():
    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()

    if not name:
        return jsonify({"error": "Falta el nombre"}), 400

    saludo_template = random.choice(SALUDOS)
    saludo = saludo_template.format(name=name)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO greetings (name, created_at) VALUES (?, ?)",
        (name, datetime.utcnow().isoformat())
    )

    cursor.execute("SELECT COUNT(*) FROM greetings")
    total = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    return jsonify({
        "greeting": saludo,
        "total": total
    })

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
