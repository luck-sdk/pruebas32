from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import os
import time
import urllib.parse

app = Flask(__name__)

# =========================
# CONFIG DB AZURE SQL
# =========================
SQL_CONNECTION = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=tcp:jhe.database.windows.net,1433;"
    "DATABASE=jp;"
    "UID=LAPTOP-G2LDQUC8@jhe;"
    "PWD=jhosue@2005;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

params = urllib.parse.quote_plus(SQL_CONNECTION)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mssql+pyodbc:///?odbc_connect={params}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =========================
# MODELO
# =========================
class Medicion(db.Model):
    __tablename__ = "mediciones"

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, server_default=func.current_timestamp())
    alcohol = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "fecha": str(self.fecha),
            "alcohol": self.alcohol
        }

# =========================
# HOME
# =========================
@app.route("/")
def home():
    return jsonify({"status": "OK", "msg": "API lista 🚀"})

# =========================
# INSERTAR (ESP32 / JS / APP)
# =========================
@app.route("/mediciones", methods=["POST"])
def insertar():
    data = request.get_json()

    if not data or "alcohol" not in data:
        return jsonify({"error": "Falta alcohol"}), 400

    alcohol = float(data["alcohol"])

    nuevo = Medicion(alcohol=alcohol)
    db.session.add(nuevo)
    db.session.commit()

    return jsonify(nuevo.to_dict()), 201

# =========================
# LISTAR
# =========================
@app.route("/mediciones", methods=["GET"])
def listar():
    datos = Medicion.query.order_by(Medicion.id.desc()).all()
    return jsonify([d.to_dict() for d in datos])

# =========================
# ULTIMO
# =========================
@app.route("/mediciones/ultima", methods=["GET"])
def ultima():
    dato = Medicion.query.order_by(Medicion.id.desc()).first()
    return jsonify(dato.to_dict() if dato else {})

# =========================
# HEALTH (IMPORTANTE AZURE)
# =========================
@app.route("/health")
def health():
    try:
        db.session.execute("SELECT 1")
        return jsonify({"status": "OK", "db": "connected"})
    except Exception as e:
        return jsonify({"status": "ERROR", "msg": str(e)}), 500


# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)