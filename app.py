from fastapi import FastAPI
import pyodbc
from datetime import datetime

app = FastAPI()

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

@app.get("/")
def home():
    return {"status": "OK", "time": str(datetime.now())}

@app.post("/mediciones")
def insertar(data: dict):
    alcohol = float(data["alcohol"])

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO mediciones (alcohol) VALUES (?)",
        alcohol
    )

    conn.commit()
    conn.close()

    return {"status": "ok", "alcohol": alcohol}

@app.get("/mediciones")
def listar():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT TOP 50 id, fecha, alcohol FROM mediciones ORDER BY id DESC")
    rows = cur.fetchall()

    conn.close()

    return [
        {"id": r[0], "fecha": str(r[1]), "alcohol": r[2]}
        for r in rows
    ]
