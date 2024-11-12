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
        name = data.get('Name')
        description = data.get('Description')
        price = data.get('Price')
        categories_id = data.get('Categories_ID')  # Este puede ser None
        size_id = data.get('Size_ID')  # Este puede ser None
        color_id = data.get('color_ID')  # Este puede ser None
        brand_id = data.get('Brand_ID')  # Este puede ser None
        year_id = data.get('Year_ID')  # Este puede ser None
        image = data.get('image')  # Este puede ser None

        # Verifica si los parámetros obligatorios están presentes
        if not all([name, description, price]):
            return jsonify({"error": "Faltan parámetros obligatorios"}), 400

        # Si los parámetros opcionales son None, se pueden insertar como NULL en la base de datos
        qagregar = """INSERT INTO products(Name, Description, Price, Categories_ID, 
                                            Size_ID, color_ID, Brand_ID, Year_ID, image) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        
        # Ejecuta la inserción con los valores, permitiendo que algunos valores sean None (NULL)
        cur.execute(qagregar, (name, description, price, categories_id, size_id, 
                               color_id, brand_id, year_id, image))
        mari.commit()
        return jsonify({"message": "Producto creado exitosamente"}), 201

    except mariadb.Error as e:
        return jsonify({"error": "Error en la base de datos", "message": str(e)}), 500
    
    finally:
        if mari:
            mari.close()

