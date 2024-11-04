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
@app.route("/users/<int:id>", methods=('POST', 'DELETE'))
def borrarProducto(id):
    mari = mariadb.connect(
        user="uniondepo",
        password="uniondepo111",
        host="10.9.120.5",
        database="uniondepo"
    )
    cur = mari.cursor()
    sentSql1 = """SELECT u.name, u.lastname, u.email, u.password, u.address, u.phone_number, c.comuna, r.rol FROM users u 
                    INNER JOIN comunas c ON c.ID = u.Comuna_id 
                    INNER JOIN rols r on r.ID = c.ID;"""
    cur.execute(sentSql1, (id,))
    usuario = [column[0] for column in cur.description]
    usuario_data = cur.fetchall()

    if not usuario_data:
        return jsonify({"error": "usuario no encontrado"}), 404

    tabla = [dict(zip(usuario, row)) for row in usuario_data]

    if request.method == 'POST':
        qagregar = """INSERT INTO users(name, email, password) value(? , ? , ? );"""
        cur.execute(qagregar, (id, ))
        mari.commit()
        return jsonify({"message": "usuario creado exitosamente"}), 200


    if request.method == 'DELETE':
        qborrar = """DELETE FROM users WHERE ID=?"""
        cur.execute(qborrar, (id,))
        mari.commit()
        return jsonify({"message": "usuario borrado exitosamente"}), 200
    
    return jsonify(tabla)