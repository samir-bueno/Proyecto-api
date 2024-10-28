from flask import Flask, jsonify, request
import mariadb

app = Flask(__name__)

def conectar_db():
    """Conectar a la base de datos y devolver la conexión."""
    return mariadb.connect(
        user="uniondepo",
        password="uniondepo111",
        host="10.9.120.5",
        database="uniondepo"
    )

@app.route("/products")
def Productos():
    mari = mariadb.connect(
        user = "uniondepo",
        password ="uniondepo111",
        host ="10.9.120.5",
        database= "uniondepo"
    )
    cur = mari.cursor()
    cur.execute("SELECT * FROM products")

    color = [column[0] for column in cur.description]
    
    tabla = []
    for row in cur:
        tabla.append(dict(zip(color, row)))

    return jsonify(tabla)



@app.route('/insertar', methods=['POST'])
def insertar_producto():
    data = request.json
    nombre = data.get('Name')
    precio = data.get('Price')

    try:
        mari = conectar_db()
        cur = mari.cursor()
        sql_insert_query = """INSERT INTO products (Name, Price)
                              VALUES (?, ?)"""
        cur.execute(sql_insert_query, (nombre, precio))
        mari.commit()
        return jsonify({"mensaje": f"Producto '{nombre}' insertado correctamente."}), 201

    except mariadb.Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if mari:
            cur.close()
            mari.close()


if __name__ == '__main__':
    app.run(debug=True)
