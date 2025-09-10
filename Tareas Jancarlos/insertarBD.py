import cnx 
from pymysql import Error 

try:
    conectar = cnx.camino #a la variable conectar le pasamos la cadena de conexion
    consulta = conectar.cursor()#cursor sirve para trabajas con consultas SQL
    #Ahora vamos a definir los datos que vamos a ingresar
    nombre = "Ever"
    Pasw= "hola"
    correo = "ever@gmail.com"
    #Vamos a definir la consulta para insertar los datos
    InsertarSQL = "INSERT INTO usuarios(nombre, email, PASSWORD)VALUES(%s,%s,%s)"
    valores = (nombre, correo, Pasw)
    consulta.execute (InsertarSQL, valores)#execute sirve para enviar los datos a las BD
    conectar.commit()#Commit guarda los cambios en la BD
    print("Datos almacenados correctamente")
except Error as e:
    print("Error al guardar los datos", e)
finally:
    cnx.camino.close()
    print("La conexion fue cerrada")