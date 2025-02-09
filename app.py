from flask import Flask, render_template, request
import pymysql

# Conexión a MySQL con pymysql (adpta los parámetros a tu servidor local)
def get_db_connection():
    return pymysql.connect(
        host="10.3.29.20",
        port=33060,
        user="user_agenda_db",
        password="usuario",
        database="agenda_db",
    )

app = Flask(__name__)

@app.route("/")
def menu():
    return render_template("home.html")

@app.route("/listar")
def listar():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT nombre, telefono FROM contactos")
        contactos = cursor.fetchall()
    connection.close()
    return render_template("listar.html", contactos=contactos)
    

@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    mensaje=""
    resultado = ()

    if request.method == "POST":
        nombre = request.form["nombre"]
        if nombre:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT nombre, telefono FROM contactos where nombre = %s", (nombre))
                contactos = cursor.fetchall()
                if len(contactos) == 0:
                    resultado = ()
                    mensaje = "Contacto no encontrado."
                connection.close()
                resultado = contactos
        else:
            resultado = ()
            mensaje = "No has introducido ningún nombre."
        
    return render_template("buscar.html", resultado=resultado, mensaje=mensaje)

@app.route("/insertar", methods=["GET", "POST"])
def insertar():
    mensaje = ""

    if request.method == "POST":
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("insert into contactos (nombre, telefono) values (%s, %s)", (nombre, telefono))
            mensaje = f"Contacto {nombre} insertado."
        connection.commit()
        connection.close()

    return render_template("insertar.html", mensaje=mensaje)

@app.route("/borrar", methods=["GET", "POST"])
def borrar():
    mensaje = ""

    if request.method == "POST":
        nombre = request.form["nombre"]
        if nombre:
            connection = get_db_connection()
            # Existe el contacto?
            with connection.cursor() as cursor:
                cursor.execute("SELECT nombre, telefono FROM contactos where nombre = %s", (nombre))
                contactos = cursor.fetchall()
            if len(contactos) == 0:
                mensaje = "Contacto no encontrado."
            else:
                # No existe, borrar
                with connection.cursor() as cursor:
                    cursor.execute("delete from contactos where nombre = %s", (nombre))
                    mensaje = f"Contacto {nombre} eliminado."
                connection.commit()
                connection.close()            

    return render_template("borrar.html", mensaje=mensaje)

if __name__ == "__main__":
    app.run(debug=True)
