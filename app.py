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

# Usa directamente la URL de la base de datos que configuraste en Render
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de la tabla tareas
class Tarea(db.Model):
    __tablename__ = 'tareas'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255), nullable=False)
    completada = db.Column(db.Boolean, default=False)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/tareas", methods=["GET", "POST"])
def tareas():
    if request.method == "POST":
        tarea = request.form.get("descripcion")
        if tarea:
            nueva_tarea = Tarea(descripcion=tarea)
            db.session.add(nueva_tarea)
            db.session.commit()
        return redirect("/tareas")

    tareas = Tarea.query.all()
    return render_template("tareas.html", tareas=tareas)

@app.route("/completar/<int:id>")
def completar(id):
    tarea = Tarea.query.get_or_404(id)
    tarea.completada = True
    db.session.commit()
    return redirect("/tareas")

@app.route("/acerca")
def acerca():
    return render_template("acerca.html")

@app.route("/estadisticas")
def estadisticas():
    total = Tarea.query.count()
    completadas = Tarea.query.filter_by(completada=True).count()
    pendientes = total - completadas
    return render_template("estadisticas.html", total=total, completadas=completadas, pendientes=pendientes)

if __name__ == "__main__":
    app.run(debug=True)










