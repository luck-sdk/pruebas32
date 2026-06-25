from fastapi import FastAPI, Request
import pyodbc
import os
from datetime import datetime

app = FastAPI()

# =========================
# CONEXIÓN SQL (AZURE)
# =========================
CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=tcp:jhe.database.windows.net,1433;"
    "DATABASE=jp;"
    "UID=LAPTOP-G2LDQUC8@jhe;"
    "PWD=jhosue@2005;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
)

def get_conn():
    return pyodbc.connect(CONN_STR)

# =========================
# HOME
# =========================
@app.get("/")
def home():
    return {
        "status": "OK",
        "message": "FAST API RUNNING 🚀",
        "time": str(datetime.now())
    }

# =========================
# INSERT (ESP32)
# =========================
@app.post("/mediciones")
async def insertar(request: Request):
    data = await request.json()
    alcohol = float(data["alcohol"])

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO mediciones (alcohol) VALUES (?)",
        alcohol
    )

    conn.commit()
    conn.close()

    return {"status": "ok", "alcohol": alcohol}

# =========================
# LISTAR
# =========================
@app.get("/mediciones")
def listar():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT TOP 50 id, fecha, alcohol FROM mediciones ORDER BY id DESC")
    rows = cursor.fetchall()

    conn.close()

    return [
        {"id": r[0], "fecha": str(r[1]), "alcohol": r[2]}
        for r in rows
    ]

# =========================
# ULTIMO DATO (MUY RÁPIDO)
# =========================
@app.get("/mediciones/ultima")
def ultima():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT TOP 1 id, fecha, alcohol FROM mediciones ORDER BY id DESC")
    r = cursor.fetchone()

    conn.close()

    if not r:
        return {"msg": "sin datos"}

    return {"id": r[0], "fecha": str(r[1]), "alcohol": r[2]}
