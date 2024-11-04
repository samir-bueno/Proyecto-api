from flask import Flask, jsonify, request
from flask_cors import CORS
import mariadb

app = Flask(__name__)
CORS(app)

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

# Permite crear un nuevo producto
@app.route("/products", methods=['POST'])
def crearProducto():
    # Establece la conexión a la base de datos
    try:
        mari = mariadb.connect(
            user="uniondepo",
            password="uniondepo111",
            host="10.9.120.5",
            database="uniondepo"
        )
        cur = mari.cursor()
        
        # Obtén los datos del cuerpo de la solicitud
        data = request.json
        print("Datos recibidos:", data)  # Para depuración

        name = data.get('Name')
        description = data.get('Description')
        price = data.get('Price')
        categories_id = data.get('Categories_ID')
        size_id = data.get('Size_ID')
        color_id = data.get('color_ID')
        brand_id = data.get('Brand_ID')
        year_id = data.get('Year_ID')
        image = data.get('image')  # Puede ser None si no se proporciona

        # Verifica si todos los parámetros requeridos están presentes
        if all([name, description, price is not None, categories_id is not None,
                size_id is not None, color_id is not None, brand_id is not None,
                year_id is not None]):
            
            # Inserta el nuevo producto
            qagregar = """INSERT INTO products(Name, Description, Price, Categories_ID, 
                                                Size_ID, color_ID, Brand_ID, Year_ID, image) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            cur.execute(qagregar, (name, description, price, categories_id, 
                                    size_id, color_id, brand_id, year_id, image))
            mari.commit()
            return jsonify({"message": "Producto creado exitosamente"}), 201
        else:
            return jsonify({"error": "Faltan parámetros"}), 400

    except mariadb.Error as e:
        print("Error al conectar a la base de datos:", e)
        return jsonify({"error": "Error en el servidor."}), 500

    finally:
        if mari:
            mari.close()
