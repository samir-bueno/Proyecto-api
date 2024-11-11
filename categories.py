from flask import Flask, jsonify
from flask_cors import CORS
import mariadb

app = Flask(__name__)
CORS(app)  # Esto permite todas las solicitudes CORS desde cualquier origen

@app.route("/categories")
def Colores():
    mari = mariadb.connect(
        user = "uniondepo",
        password ="uniondepo111",
        host ="10.9.120.5",
        database= "uniondepo"
    )
    cur = mari.cursor()
    cur.execute("SELECT * FROM categories")

    color = [column[0] for column in cur.description]
    
    tabla = []
    for row in cur:
        tabla.append(dict(zip(color, row)))

    return jsonify(tabla)


@app.route("/categories/<int:id>")
def Tarta(id):
    mari = mariadb.connect(
        user = "uniondepo",
        password ="uniondepo111",
        host ="10.9.120.5",
        database= "uniondepo"
    )
    cur = mari.cursor()
    cur.execute("SELECT * FROM categories WHERE ID= ?", (id,))

    color = [column[0] for column in cur.description]
    
    tabla = [dict(zip(color, row)) for row in cur.fetchall()]

    return jsonify(tabla)

