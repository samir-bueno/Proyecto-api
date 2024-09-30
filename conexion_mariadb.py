import mariadb

# Conectar a la base de datos
maria = mariadb.connect(
    user="uniondepo",
    password="uniondepo111",
    host="10.9.120.5",
    database="uniondepo"
)

cur = maria.cursor()
cur.execute("SELECT * FROM users")

# Obtener los nombres de las columnas
users = [column[0] for column in cur.description]

# Almacenar los resultados en una lista de diccionarios
tabla = []
for row in cur:
    tabla.append(dict(zip(users, row)))

# Cerrar la conexión
maria.close()

# Imprimir los resultados
print(tabla)
