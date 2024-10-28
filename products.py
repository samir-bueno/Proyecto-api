from flask import Flask, jsonify, request
from flask_cors import CORS
import mariadb
from mariadb import Error
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

<<<<<<< HEAD
if __name__ == '__main__':
    app.run(debug=True)
=======

from flask import jsonify
import mariadb
from mariadb import Error

@app.route("/products45/<name>")
def buscar_producto(name):
    try:
        # Establecer conexión a la base de datos
        mari = mariadb.connect(
            user="uniondepo",
            password="uniondepo111",
            host="10.9.120.5",
            database="uniondepo"
        )
        cursor = mari.cursor()  # Crear un cursor para ejecutar consultas

        sql_select_query = """SELECT * FROM products WHERE Name LIKE %s"""
        cursor.execute(sql_select_query, ('%' + name + '%',))
        resultados = cursor.fetchall()

        if resultados:
            productos = [
                {"ID": producto[0], "Nombre": producto[1], "Precio": producto[2], "Cantidad": producto[3]}
                for producto in resultados
            ]
            return jsonify(productos)  # Retornar resultados en formato JSON
        else:
            return jsonify({"message": "No se encontraron productos."}), 404  # Manejo de no coincidencias
    except Error as e:
        return jsonify({"error": f"Error al conectar a la base de datos: {e}"}), 500  # Manejo de errores
    finally:
        # Cerrar conexiones y cursores
        if 'mari' in locals():
            cursor.close()
            mari.close()

>>>>>>> 05446c63bc989200fcef43db7ede5beb1c805438
