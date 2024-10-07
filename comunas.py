from flask import Flask, jsonify
import mariadb

app = Flask(__name__)

@app.route("/comunas")
def comunas():
    mari = mariadb.connect(
        user = "uniondepo",
        password ="uniondepo111",
        host ="10.9.120.5",
        database= "uniondepo"
    )
    cur = mari.cursor()
    cur.execute("SELECT * FROM comunas")

    comuna = [column[0] for column in cur.description]
    
    tabla = []
    for row in cur:
        tabla.append(dict(zip(comuna, row)))

    return jsonify(tabla)


@app.route("/comunas/<int:id>")
def detalle_comuna(id):
    mari = mariadb.connect(
        user = "uniondepo",
        password ="uniondepo111",
        host ="10.9.120.5",
        database= "uniondepo"
    )
    cur = mari.cursor()
    cur.execute("SELECT * FROM comunas WHERE ID= ?", (id,))

    comuna = [column[0] for column in cur.description]
    
    tabla = [dict(zip(comuna, row)) for row in cur.fetchall()]

    return jsonify(tabla)
