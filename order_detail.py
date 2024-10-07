from flask import Flask, jsonify
import mariadb

app = Flask(__name__)

@app.route("/order-detail")
def Order_detail():
    mari = mariadb.connect(
        user = "uniondepo",
        password ="uniondepo111",
        host ="10.9.120.5",
        database= "uniondepo"
    )
    cur = mari.cursor()
    cur.execute("SELECT * FROM order_detail")

    order_detail = [column[0] for column in cur.description]
    
    tabla = []
    for row in cur:
        tabla.append(dict(zip(order_detail, row)))

    return jsonify(tabla)


@app.route("/order-detail/<int:id>")
def Tarta(id):
    mari = mariadb.connect(
        user = "uniondepo",
        password ="uniondepo111",
        host ="10.9.120.5",
        database= "uniondepo"
    )
    cur = mari.cursor()
    cur.execute("SELECT * FROM order_detail WHERE ID= ?", (id,))

    order_detail = [column[0] for column in cur.description]
    
    tabla = [dict(zip(order_detail, row)) for row in cur.fetchall()]

    return jsonify(tabla)

