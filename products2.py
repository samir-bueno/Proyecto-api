from flask import Flask, jsonify, request
import mariadb

app = Flask(__name__)

@app.route("/products2")
def Productos():
    pagina = None
    filtro = None
    elementos_por_pagina = 8  # Define this to avoid uninitialized variable error

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
            query = "SELECT * FROM products"
            cur.execute(query)
        else:
            paginas_descartadas = pagina - 1
            elementos_descartados = paginas_descartadas * elementos_por_pagina
            query = "SELECT * FROM products ORDER BY Year_ID DESC LIMIT ? OFFSET ?"
            cur.execute(query, (elementos_por_pagina, elementos_descartados))
    else:
        # You might want to implement the filtering logic here
        # Assuming filtering is not implemented, just return all results
        query = "SELECT * FROM products"
        cur.execute(query)

    producto = [column[0] for column in cur.description]
    
    tabla = [dict(zip(producto, row)) for row in cur.fetchall()]

    return jsonify(tabla)