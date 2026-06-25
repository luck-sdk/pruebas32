from flask import Flask, request, jsonify
import pyodbc
import os
import time

app = Flask(__name__)

# ======================
# CONEXIÓN AZURE SQL
# ======================
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

# ======================
# HOME
# ======================
@app.route("/")
def home():
    return {"status": "OK", "msg": "API funcionando"}

# ======================
# INSERTAR DATOS (ESP32)
# ======================
@app.route("/mediciones", methods=["POST"])
def insertar():
    data = request.get_json()

    if "alcohol" not in data:
        return {"error": "Falta alcohol"}, 400

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

# ======================
# OBTENER DATOS
# ======================
@app.route("/mediciones", methods=["GET"])
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

# ======================
# ÚLTIMO DATO
# ======================
@app.route("/mediciones/ultima", methods=["GET"])
def ultima():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT TOP 1 id, fecha, alcohol FROM mediciones ORDER BY id DESC")
    r = cursor.fetchone()

    conn.close()

    if not r:
        return {"msg": "sin datos"}

    return {"id": r[0], "fecha": str(r[1]), "alcohol": r[2]}

# ======================
# RUN
# ======================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
