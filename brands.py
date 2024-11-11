from flask import Flask, jsonify
from flask_cors import CORS
import mariadb

app = Flask(__name__)
CORS(app)

@app.route("/brands")
def brands():
    mari = mariadb.connect(
        user = "uniondepo",
        password ="uniondepo111",
        host ="10.9.120.5",
        database= "uniondepo"
    )
    cur = mari.cursor()
    cur.execute("SELECT * FROM brands")

    color = [column[0] for column in cur.description]
    
    tabla = []
    for row in cur:
        tabla.append(dict(zip(color, row)))

    return jsonify(tabla)


@app.route("/brands/<int:id>")
def detalle_brands(id):
    mari = mariadb.connect(
        user = "uniondepo",
        password ="uniondepo111",
        host ="10.9.120.5",
        database= "uniondepo"
    )
    cur = mari.cursor()
    cur.execute("SELECT * FROM brands WHERE ID= ?", (id,))

    color = [column[0] for column in cur.description]
    
    tabla = [dict(zip(color, row)) for row in cur.fetchall()]

    return jsonify(tabla)