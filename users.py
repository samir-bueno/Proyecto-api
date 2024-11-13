
from flask import Flask, jsonify, request
from flask_cors import CORS
import mariadb
from mariadb import Error

app = Flask(__name__)
CORS(app)

@app.route("/users", methods=['POST'])
def users():
    try:
        mari = mariadb.connect(
            user="uniondepo",
            password="uniondepo111",
            host="10.9.120.5",
            database="uniondepo"
        )
        cur = mari.cursor()

        if request.method == 'POST':
            # Obtén los datos del cuerpo de la solicitud
            data = request.json
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')

            # Validación de los datos
            if not name or not email or not password:
                return jsonify({"error": "Faltan parámetros"}), 400

            # Comprobar si el usuario ya existe
            cur.execute("SELECT * FROM users WHERE email = ?", (email,))
            existing_user = cur.fetchone()
            if existing_user:
                return jsonify({"error": "El usuario ya existe con ese correo electrónico"}), 400

            # Insertar el nuevo usuario
            query = """INSERT INTO users (name, email, password) VALUES (?, ?, ?)"""
            cur.execute(query, (name, email, password))
            mari.commit()

            return jsonify({"message": "Usuario creado exitosamente"}), 201

    except Error as e:
        return jsonify({"error": f"Error al conectar con la base de datos: {str(e)}"}), 500

    finally:
        if mari:
            mari.close()

    return jsonify({"error": "Método no permitido"}), 405

if __name__ == "__main__":
    app.run(debug=True)


@app.route("/login", methods=['POST'])
def login():
    try:
        mari = mariadb.connect(
            user="uniondepo",
            password="uniondepo111",
            host="10.9.120.5",
            database="uniondepo"
        )
        cur = mari.cursor()

        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Faltan parámetros"}), 400

        # Verificar las credenciales del usuario
        cur.execute("SELECT name, email, Rol_ID FROM users WHERE email = ? AND password = ?", (email, password))
        user = cur.fetchone()

        if user:
            # Si el usuario existe, enviar el objeto con isAdmin
            return jsonify({
                "message": "Inicio de sesión exitoso",
                "usuario": {
                    "name": user[0],
                    "email": user[1],
                    "Rol_ID": user[2]  # Incluir isAdmin
                }
            }), 200
        else:
            return jsonify({"error": "Credenciales incorrectas"}), 401

    except Error as e:
        return jsonify({"error": f"Error al conectar con la base de datos: {str(e)}"}), 500

    finally:
        if mari:
            mari.close()


if __name__ == "__main__":
    app.run(debug=True)





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

