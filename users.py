from flask import Flask, jsonify, request
from flask_cors import CORS
import mariadb
from mariadb import Error

app = Flask(__name__)
CORS(app)

@app.route("/users")
def users():
    mari = mariadb.connect(
        user="uniondepo",
        password="uniondepo111",
        host="10.9.120.5",
        database="uniondepo"
    )
    cur = mari.cursor()
    cur.execute("SELECT * FROM users")

    color = [column[0] for column in cur.description]
    
    tabla = []
    for row in cur:
        row_data = {}
        for col_name, value in zip(color, row):
            if isinstance(value, bytes):
                # Omitir la columna si es de tipo bytes
                continue
            row_data[col_name] = value
        tabla.append(row_data)

    return jsonify(tabla)


# Selecciona un producto y permite borrar
@app.route("/users/<int:id>", methods=('GET', 'POST', 'DELETE'))
def manejar_usuario(id):
    mari = mariadb.connect(
        user="uniondepo",
        password="uniondepo111",
        host="10.9.120.5",
        database="uniondepo"
    )
    cur = mari.cursor()

    if request.method == 'GET':
        sentSql1 = """SELECT name, email, password FROM users WHERE ID = ?"""
        cur.execute(sentSql1, (id,))
        usuario_data = cur.fetchall()

        if not usuario_data:
            return jsonify({"error": "usuario no encontrado"}), 404

        # Convertir a un diccionario y manejar posibles bytes
        tabla = []
        for row in usuario_data:
            user_dict = {
                "name": row[0],
                "email": row[1],
                "password": row[2].decode('utf-8') if isinstance(row[2], bytes) else row[2]
            }
            tabla.append(user_dict)

        return jsonify(tabla), 200

    if request.method == 'POST':
        data = request.json  # Obtén los datos del cuerpo de la solicitud
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if name and email and password:
            qagregar = """INSERT INTO users(name, email, password) VALUES (?, ?, ?)"""
            cur.execute(qagregar, (name, email, password))
            mari.commit()
            return jsonify({"message": "usuario creado exitosamente"}), 201
        else:
            return jsonify({"error": "Faltan parámetros"}), 400

    if request.method == 'DELETE':
        qborrar = """DELETE FROM users WHERE ID=?"""
        cur.execute(qborrar, (id,))
        mari.commit()
        return jsonify({"message": "usuario borrado exitosamente"}), 200

    return jsonify({"error": "Método no permitido"}), 405
