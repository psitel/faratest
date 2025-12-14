from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sqlite3
import random
from datetime import datetime

app = FastAPI()

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

class NameRequest(BaseModel):
    name: str

DB_PATH = "database.db"

SALUDOS = [
    "Hola {name}",
    "¿Qué tal {name}?",
    "¿Qué hay, {name}?",
    "Encantado de verte, {name}",
    "Buenas, {name}",
    "Ey {name}, ¿todo bien?",
    "Saludos, {name}",
    "Bienvenido, {name}"
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

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return FileResponse("frontend/index.html")

@app.post("/api/greet")
def greet(payload: NameRequest):
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Falta el nombre")

    saludo = random.choice(SALUDOS).format(name=name)

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

    return {
        "greeting": saludo,
        "total": total
    }
