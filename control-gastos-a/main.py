import sqlite3
from datetime import datetime
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Control de Gastos")
DB_NAME = "gastos.db"

# --- Modelos de datos ---
class TransaccionCreate(BaseModel):
    descripcion: str
    monto: float
    tipo: str  # "ingreso" o "gasto"
    categoria: str

class Transaccion(TransaccionCreate):
    id: int
    fecha: str

# --- Inicialización de la Base de Datos ---
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transacciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion TEXT NOT NULL,
                monto REAL NOT NULL,
                tipo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                fecha TEXT NOT NULL
            )
        """)

init_db()

# --- Rutas de la API ---
@app.get("/", response_class=HTMLResponse)
def servir_frontend():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/transacciones", response_model=List[Transaccion])
def listar_transacciones():
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("SELECT * FROM transacciones ORDER BY id DESC")
        return [dict(row) for row in cursor.fetchall()]

@app.post("/api/transacciones", response_model=Transaccion)
def crear_transaccion(tx: TransaccionCreate):
    if tx.monto <= 0:
        raise HTTPException(status_code=400, detail="El monto debe ser mayor a 0")
    if tx.tipo not in ["ingreso", "gasto"]:
        raise HTTPException(status_code=400, detail="El tipo debe ser 'ingreso' o 'gasto'")
    
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute(
            "INSERT INTO transacciones (descripcion, monto, tipo, categoria, fecha) VALUES (?, ?, ?, ?, ?)",
            (tx.descripcion, tx.monto, tx.tipo, tx.categoria, fecha_actual)
        )
        nuevo_id = cursor.lastrowid
        return {**tx.model_dump(), "id": nuevo_id, "fecha": fecha_actual}

@app.delete("/api/transacciones/{tx_id}")
def eliminar_transaccion(tx_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute("DELETE FROM transacciones WHERE id = ?", (tx_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return {"mensaje": "Eliminado correctamente"}
