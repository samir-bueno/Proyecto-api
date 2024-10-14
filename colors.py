from flask import Flask, jsonify, request
import mariadb

app = Flask(__name__)

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


@app.route("/colors/<int:id>")
def Tarta(id):
    mari = mariadb.connect(
        user="uniondepo",
        password="uniondepo111",
        host="10.9.120.5",
        database="uniondepo"
    )
    cur = mari.cursor()
    cur.execute("SELECT * FROM color WHERE ID= ?", (id,))

    color = [column[0] for column in cur.description]
    
    tabla = [dict(zip(color, row)) for row in cur.fetchall()]

    return jsonify(tabla)

if __name__ == "__main__":
    app.run(debug=True)
