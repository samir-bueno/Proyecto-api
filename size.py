from flask import Flask, jsonify, request
from flask_cors import CORS
import mariadb

app = Flask(__name__)
CORS(app)

# Muestra todos los productos
@app.route("/sizes", methods=["GET"])
def sizes():
    mari = mariadb.connect(
        user="uniondepo",
        password="uniondepo111",
        host="10.9.120.5",
        database="uniondepo"
    )
    cur = mari.cursor()
    cur.execute("SELECT * FROM size")

    color = [column[0] for column in cur.description]
    
    tabla = []
    for row in cur:
        tabla.append(dict(zip(color, row)))

    return jsonify(tabla)