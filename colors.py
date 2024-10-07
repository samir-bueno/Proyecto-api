from flask import Flask, jsonify
import mariadb

app = Flask(__name__)

@app.route("/colors")
def Colores():
    mari = mariadb.connect(
        user = "uniondepo",
        password ="uniondepo111",
        host ="10.9.120.5",
        database= "uniondepo"
    )
    cur = mari.cursor()
    cur.execute("SELECT * FROM color")

    color = [column[0] for column in cur.description]
    
    tabla = []
    for row in cur:
        tabla.append(dict(zip(color, row)))

    return jsonify(tabla)


@app.route("/colors/<int:id>")
def Tarta(id):
    mari = mariadb.connect(
        user = "uniondepo",
        password ="uniondepo111",
        host ="10.9.120.5",
        database= "uniondepo"
    )
    cur = mari.cursor()
    cur.execute("SELECT * FROM color WHERE ID= ?", (id,))

    color = [column[0] for column in cur.description]
    
    tabla = [dict(zip(color, row)) for row in cur.fetchall()]

    return jsonify(tabla)

