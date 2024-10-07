from flask import Flask, jsonify
import mariadb

app = Flask(__name__)

@app.route("/order")
def orders():
    mari = mariadb.connect(
        user = "uniondepo",
        password ="uniondepo111",
        host ="10.9.120.5",
        database= "uniondepo"
    )
    cur = mari.cursor()
    cur.execute("SELECT * FROM orders")

    Orders = [column[0] for column in cur.description]
    
    tabla = []
    for row in cur:
        tabla.append(dict(zip(Orders, row)))

    return jsonify(tabla)


@app.route("/order/<int:id>")
def detalle_orders(id):
    mari = mariadb.connect(
        user = "uniondepo",
        password ="uniondepo111",
        host ="10.9.120.5",
        database= "uniondepo"
    )
    cur = mari.cursor()
    cur.execute("SELECT * FROM brands WHERE ID= ?", (id,))

    ordenes = [column[0] for column in cur.description]
    
    tabla = [dict(zip(ordenes, row)) for row in cur.fetchall()]

    return jsonify(tabla)