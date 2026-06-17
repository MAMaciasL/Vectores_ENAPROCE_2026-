import mysql.connector

# conexión
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="empresa"
)

cursor = conexion.cursor()