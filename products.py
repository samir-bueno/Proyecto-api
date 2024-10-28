from flask import Flask, jsonify, request
from flask_cors import CORS
import mariadb

app = Flask(__name__)

# Configurar CORS
CORS(app)  # Permitir todos los orígenes

# Muestra todos los productos
@app.route("/products")
def Productos():
    mari = mariadb.connect(
        user="uniondepo",
        password="uniondepo111",
        host="10.9.120.5",
        database="uniondepo"
    )
    cur = mari.cursor()
    cur.execute("SELECT * FROM products")

    color = [column[0] for column in cur.description]
    
    tabla = []
    for row in cur:
        tabla.append(dict(zip(color, row)))

    return jsonify(tabla)

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

# Selecciona un producto y permite borrar
@app.route("/products/<int:id>", methods=('GET', 'DELETE'))
def borrarProducto(id):
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
    producto_data = cur.fetchall()

    if not producto_data:
        return jsonify({"error": "Producto no encontrado"}), 404

    curC = mari.cursor()
    sentSql2 = """SELECT * FROM size WHERE ID= ?"""
    curC.execute(sentSql2, (id,))
    size = [column[0] for column in curC.description]
    size_data = curC.fetchall()

    tabla = [dict(zip(producto, row)) for row in producto_data]
    tablaSize = [dict(zip(size, row)) for row in size_data]

    if request.method == 'DELETE':
        qborrar = """DELETE FROM products WHERE ID=?"""
        cur.execute(qborrar, (id,))
        mari.commit()
        return jsonify({"message": "Producto borrado exitosamente"}), 200
    
    return jsonify(tabla, tablaSize)

if __name__ == '__main__':
    app.run(debug=True)
