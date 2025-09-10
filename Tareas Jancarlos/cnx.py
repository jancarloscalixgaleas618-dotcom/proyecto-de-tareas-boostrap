import pymysql
from pymysql import Error

try:
    camino = pymysql.connect(
        host="localhost",
        user= "root",
        password= "",
        database= "pw1"
    )
    print("conexion exitosa")
except Error as e:
    print("Error en la conexion", e)