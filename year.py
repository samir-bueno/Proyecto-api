from flask import Flask, jsonify
from flask_cors import CORS
import mariadb

app = Flask(__name__)
CORS(app)

@app.route("/years")
def Years():
    mari = mariadb.connect(
        user = "uniondepo",
        password ="uniondepo111",
        host ="10.9.120.5",
        database= "uniondepo"
    )
    cur = mari.cursor()
    cur.execute("SELECT * FROM years")

    year = [column[0] for column in cur.description]
    
    tabla = []
    for row in cur:
        tabla.append(dict(zip(year, row)))

    return jsonify(tabla)


@app.route("/years/<int:id>")
def Tarta(id):
    mari = mariadb.connect(
        user = "uniondepo",
        password ="uniondepo111",
        host ="10.9.120.5",
        database= "uniondepo"
    )
    cur = mari.cursor()
    cur.execute("SELECT  * FROM years WHERE ID = ?", (id,))

    años = [column[0] for column in cur.description]
    
    tabla = [dict(zip(años, row)) for row in cur.fetchall()]

    return jsonify(tabla)