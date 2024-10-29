from flask import Flask, jsonify, request
from flask_cors import CORS
import mariadb
from mariadb import Error
app = Flask(__name__)
CORS(app)  # Permitir todos los orígenes

# Selecciona un producto
@app.route("/products/<int:id>")
def UnProducto(id):
    mari = mariadb.connect(
        user="uniondepo",
        password="uniondepo111",
        host="10.9.120.5",
        database="uniondepo"
    )
    cur = mari.cursor()
    sentSql1 = """SELECT Name, image, Description, Price, Sizes FROM products s  
                  INNER JOIN size t ON t.ID = s.Size_ID WHERE s.ID= ?"""
    cur.execute(sentSql1, (id,))
    producto = [column[0] for column in cur.description]
    
    curC = mari.cursor()
    sentSql2 = """SELECT * FROM size WHERE ID= ?"""
    curC.execute(sentSql2, (id,))
    size = [column[0] for column in curC.description]
    
    tabla = [dict(zip(producto, row)) for row in cur.fetchall()]
    tablaSize = [dict(zip(size, row)) for row in curC.fetchall()]
    
    return jsonify(tabla, tablaSize)