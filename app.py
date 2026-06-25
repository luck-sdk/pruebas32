from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import os
import time

app = Flask(__name__)

# ======================
# DB CONFIG (Azure SQL)
# ======================
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "SQL_CONNECTION",
    "mssql+pyodbc:///?odbc_connect=DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:jhe.database.windows.net,1433;DATABASE=jp;UID=LAPTOP-G2LDQUC8@jhe;PWD=jhosue@2005;Encrypt=yes"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ======================
# MODEL
# ======================
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

# ======================
# ROUTES
# ======================
@app.route("/")
def home():
    return jsonify({"status": "OK", "msg": "API funcionando"})

@app.route("/mediciones", methods=["POST"])
def insertar():
    data = request.get_json()
    nuevo = Medicion(alcohol=float(data["alcohol"]))
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(nuevo.to_dict())

@app.route("/mediciones", methods=["GET"])
def listar():
    datos = Medicion.query.order_by(Medicion.id.desc()).all()
    return jsonify([d.to_dict() for d in datos])

# ======================
# RUN (IMPORTANTE AZURE)
# ======================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
