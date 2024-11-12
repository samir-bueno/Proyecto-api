from flask import Flask, jsonify, request
from flask_cors import CORS
import mariadb
from mariadb import Error

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

@app.route("/categories")
def Category():
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

@app.route("/colors")
def Colores():
    pagina = None
    filtro = None
    elementos_por_pagina = 5  # Define this to avoid uninitialized variable error

    if 'pagina' in request.args:
        pagina = int(request.args['pagina'])

    if request.is_json:
        if 'pagina' in request.json:
            pagina = request.json['pagina']
        if 'filtro' in request.json:
            filtro = request.json['filtro']

    mari = mariadb.connect(
        user="uniondepo",
        password="uniondepo111",
        host="10.9.120.5",
        database="uniondepo"
    )
    cur = mari.cursor()

    if filtro is None:
        if pagina is None:
            query = "SELECT * FROM color"
            cur.execute(query)
        else:
            paginas_descartadas = pagina - 1
            elementos_descartados = paginas_descartadas * elementos_por_pagina
            query = "SELECT * FROM color LIMIT ? OFFSET ?"
            cur.execute(query, (elementos_por_pagina, elementos_descartados))
    else:
        # You might want to implement the filtering logic here
        # Assuming filtering is not implemented, just return all results
        query = "SELECT * FROM color"
        cur.execute(query)

    color = [column[0] for column in cur.description]
    
    tabla = [dict(zip(color, row)) for row in cur.fetchall()]

    return jsonify(tabla)

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
