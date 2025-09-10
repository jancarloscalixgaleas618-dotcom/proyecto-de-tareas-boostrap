from flask import Flask, render_template, request, redirect
import mysql.connector

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


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        nueva = request.form.get("descripcion")
        cursor.execute("UPDATE tareas SET descripcion = %s WHERE id = %s", (nueva, id))
        conn.commit()
        conn.close()
        return redirect("/tareas")

    cursor.execute("SELECT * FROM tareas WHERE id = %s", (id,))
    tarea = cursor.fetchone()
    conn.close()
    return render_template("editar.html", tarea=tarea)


@app.route("/eliminar/<int:id>")
def eliminar(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tareas WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect("/tareas")


if __name__ == "__main__":
    app.run(debug=True)
