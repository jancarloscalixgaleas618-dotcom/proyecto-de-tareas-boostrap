from flask import Flask            # Sirve para crear la aplicación Flask
from flask import render_template  # Sirve para mostrar páginas HTML (plantillas)
from flask import request          # Sirve para leer datos enviados desde formularios
from flask import redirect         # Sirve para redirigir al usuario de una ruta a otra
from flask import url_for          # Sirve para generar URLs dinámicas
from flask_mysqldb import MySQL    # Sirve para conectar la base de datos MySQL
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)

# Configuración de SQLAlchemy usando variables de entorno (Aiven)
db_user = os.environ.get('DB_USER', 'avnadmin')
db_pass = os.environ.get('DB_PASS', 'AVNS_iS1DanfzpzXO2Kgu37R')
db_host = os.environ.get('DB_HOST', 'mysql-5e88637-jancarloscalixgaleas618-1764.l.aivencloud.com')
db_port = os.environ.get('DB_PORT', '12582')  # Puerto de Aiven
db_name = os.environ.get('DB_NAME', 'defaultdb')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Configuración de mysql.connector para consultas directas
db_config = {
    'host': db_host,
    'user': db_user,
    'password': db_pass,
    'database': db_name,
    'port': int(db_port)
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








