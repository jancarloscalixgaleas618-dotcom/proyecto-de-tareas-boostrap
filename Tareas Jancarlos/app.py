from flask import Flask            # Sirve para crear la aplicación Flask
from flask import render_template  # Sirve para mostrar páginas HTML (plantillas)
from flask import request          # Sirve para leer datos enviados desde formularios
from flask import redirect         # Sirve para redirigir al usuario de una ruta a otra
from flask import url_for          # Sirve para generar URLs dinámicas
from flask_mysqldb import MySQL    # Sirve para conectar la base de datos MySQL
import mysql.connector          #sirve para conectar

app = Flask(__name__)


db_config = {
    'host': 'localhost',
    'user': 'root',      
    'password': '',  
    'database': 'tareas_db'
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/tareas", methods=["GET", "POST"])
def tareas():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        tarea = request.form.get("descripcion")
        if tarea:
            cursor.execute("INSERT INTO tareas (descripcion) VALUES (%s)", (tarea,))
            conn.commit()
        return redirect("/tareas")

    cursor.execute("SELECT * FROM tareas")
    tareas = cursor.fetchall()
    conn.close()
    return render_template("tareas.html", tareas=tareas)

@app.route("/completar/<int:id>")
def completar(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tareas SET completada = 1 WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect("/tareas")

@app.route("/acerca")
def acerca():
    return render_template("acerca.html")




@app.route("/estadisticas")
def estadisticas():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tareas")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tareas WHERE completada = 1")
    completadas = cursor.fetchone()[0]

    pendientes = total - completadas

    conn.close()
    return render_template("estadisticas.html", total=total, completadas=completadas, pendientes=pendientes)


if __name__ == "__main__":
    app.run(debug=True)
