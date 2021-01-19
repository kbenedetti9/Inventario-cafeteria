from flask import Flask, render_template, request, session
from werkzeug.utils import secure_filename
import sqlite3
import os
import yagmail
import hashlib
import random
from flask_session import Session

app = Flask(__name__)

# app.secret_key = os.urandom(24)


SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)
FOLDER_IMAGENES = "static/Imagenes/"
EXT_VALIDAS = ["png", "jpg"]
persona = {}


@app.route("/", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/recuperar", methods=["GET"])
def recuperar():
    return render_template("recuperar.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return render_template("login.html")


@app.route("/enviar-correo", methods=["POST"])
def send_mail():
    IdUsuario = request.form["IdUsuario"]
    correo = request.form["correo"]
    clave = ""
    email = correo
    for i in range(8):
        num = random.randint(0, 9)
        clave += str(num)
    h = hashlib.sha256(clave.encode())
    pwd = h.hexdigest()
    with sqlite3.connect("cafeteria.db") as con:
        cur2 = con.cursor()
        cur2.execute("UPDATE usuarios SET clave = ? WHERE usuario = ?", [
                                 pwd, IdUsuario])
        con.commit()
    yag = yagmail.SMTP(user='proyectogrupoctic@gmail.com',password='proyectogrupoc2022*')
    yag.send(to=email, subject='Recuperar contraseña', contents=clave)
    return render_template("/login.html")

# Rutas Admin

@app.route("/home", methods=["POST", "GET"])
def homeAdmin():
    usuario = request.form["usuario"]
    contraseña = request.form["contraseña"]
    h = hashlib.sha256(contraseña.encode())
    pwd = h.hexdigest()
    try:
        with sqlite3.connect("cafeteria.db") as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM usuarios WHERE usuario =  ?", [usuario])
            row = cur.fetchone()
    except:
        return render_template("login.html", validacion="Datos incorrectos")

    if (row is None):
        return render_template("login.html", validacion="Datos incorrectos")
    else:
        if (request.method == "POST"):
            if (usuario == row["usuario"] and pwd == row["clave"] and row["admin"] == 1):
                session["user"] = usuario
                session["nombre"] = row["nombre"]
                session["id"] = row["id"]
                return render_template("homeAdmin.html", persona=row)  # aqui
            elif (usuario == row["usuario"] and pwd == row["clave"] and row["admin"] == 0):
                session["user"] = usuario
                return render_template("homeUsuario.html", rows=Listaproductos(), persona=row)
            else:
                return render_template("login.html", validacion="Datos incorrectos")
        else:
            return render_template("login.html")


@app.route("/homeAd", methods=["GET"])
def homeAd():
    if "user" in session:
        persona["usuario"] = session["user"]
        persona["nombre"] = session["nombre"]
        persona["id"] = session["id"]
        return render_template("homeAdmin.html", persona=persona)
    else:
        return render_template("login.html")


@app.route("/crudUsuario", methods=["GET"])
def crudUsuario():
    if "user" in session:
        with sqlite3.connect("cafeteria.db") as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM usuarios")
            rows = cur.fetchall()
        persona["usuario"] = session["user"]
        # Aqui
        return render_template("crudUsuario2.html", rows=rows, persona=persona)
    else:
        return render_template("login.html")


@app.route("/usuario/crear", methods=["POST"])
def crearUsuario():
    if "user" in session:
        idUsuario = request.form["ID_usuario"]
        nombreUsuario = request.form["nombre_usuario"]
        correoUsuario = request.form["correo_electronico"]
        Usuario = request.form["Usuario"]
        autenticacion = False
        admin_usuario = False
        clave = ""
        for i in range(8):
            num = random.randint(0, 9)
            clave += str(num)
        yag = yagmail.SMTP(user='proyectogrupoctic@gmail.com',
                       password='proyectogrupoc2022*')
        email = correoUsuario
        yag.send(to=email, subject='Recuperar contraseña', contents=clave)
        h = hashlib.sha256(clave.encode())
        pwd = h.hexdigest()
        with sqlite3.connect("cafeteria.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO usuarios (id,nombre,correo,usuario,clave,autenticacion, admin) VALUES (?,?,?,?,?,?,?);",
                        [idUsuario, nombreUsuario, correoUsuario, Usuario, pwd, autenticacion, admin_usuario])
            con.commit()
        texto = "Usuario creado"
        referencia = "/crudUsuario"
        return  render_template("confirmar.html", texto = texto, referencia = referencia)
    else:
        return render_template("login.html")


@app.route("/usuario/actualizar", methods=["POST"])
def actualizarUsuario():
    if "user" in session:
        idUsuario = request.form["ID_usuario"]
        nombreUsuario = request.form["nombre_usuario"]
        correoUsuario = request.form["correo_electronico"]
        Usuario = request.form["Usuario"]

        # # try:
        with sqlite3.connect("cafeteria.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE usuarios SET nombre = ?, correo = ?, usuario = ? WHERE id = ?",
                        [nombreUsuario, correoUsuario, Usuario, idUsuario])
            con.commit()
        texto = "Usuario actualizado" 
        referencia = "/crudUsuario"
        return render_template("confirmar.html", texto = texto, referencia = referencia)
        # # except:
        # #     return "NO se pudo Guardar"
    else:
        return render_template("login.html")


@app.route("/usuario/eliminar", methods=["POST"])
def eliminarUsuario():
    if "user" in session:
        idUsuario = request.form["ID_usuario"]
        with sqlite3.connect("cafeteria.db") as con:
            cur = con.cursor()
            cur.execute("DELETE from usuarios WHERE id = ?", [idUsuario])
            con.commit()
        texto = "Usuario eliminado" 
        referencia = "/crudUsuario"   
        return render_template("confirmar.html", texto = texto, referencia = referencia)
    else:
        return render_template("login.html")


@app.route("/usuario/consultar", methods=["POST"])
def consultarUsuario():
    if "user" in session:
        persona["usuario"] = session["user"]
        idUsuario = request.form["ID_busqueda"]
        # try:
        with sqlite3.connect("cafeteria.db") as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM usuarios WHERE id = ?", [idUsuario])
            row = cur.fetchone()
        return render_template("crudUsuario.html", row=row, persona = persona)
    else:
        return render_template("login.html")


@app.route("/crudProducto", methods=["GET"])
def crudProducto():
    if "user" in session:
        with sqlite3.connect("cafeteria.db") as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM productos")
            rows = cur.fetchall()
        persona["usuario"] = session["user"]
        return render_template("crudProducto.html", rows=rows, persona=persona)
    else:
        return render_template("login.html")


@app.route("/configuracionAdmin", methods=["GET"])
def configuracionAdmin():
    if "user" in session:
        persona["usuario"] = session["user"]
        return render_template("configAdmin.html", persona=persona)
    else:
        return render_template("login.html")


@app.route("/restablecerAdmin", methods=["POST", "GET"])
def reestablecer_adm():
    if "user" in session:
        persona["usuario"] = session["user"]
        persona["nombre"] = session["nombre"]
        persona["id"] = session["id"]
        contravieja = request.form["contravieja"]
        contra = request.form["contra"]
        contra2 = request.form["contra2"]
        nombre = session["user"]
        h = hashlib.sha256(contra.encode())
        pwd = h.hexdigest()
        j = hashlib.sha256(contravieja.encode())
        pwdj = j.hexdigest()
        with sqlite3.connect("cafeteria.db") as con:
            #con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(
                "SELECT clave FROM usuarios WHERE usuario = ?", [nombre])
            row = cur.fetchone()
            if row:
                clave = row[0]
        if pwdj == clave:
            if contra == contra2:
                with sqlite3.connect("cafeteria.db") as con:
                    cur2 = con.cursor()
                    cur2.execute("UPDATE usuarios SET clave = ? WHERE usuario = ?", [
                                 pwd, nombre])
                    con.commit()
                    return render_template("homeAdmin.html", persona=persona)
            else:
                validacion = "Claves Distintas"
                # Mostrar Mensaje nueva clave no coincide
                return render_template("configAdmin.html", validacion=validacion, persona=persona)
        else:
            validacion = "Antigua clave erronea"
            return render_template("configAdmin.html", validacion=validacion, persona=persona)
            # Mostrar mensaje clave antigua equivocada

    else:
        return render_template("login.html")

# Rutas Usuario


@app.route("/homeUsuario", methods=["GET"])
def homeUsuario():
    if "user" in session:
        persona["usuario"] = session["user"]
        return render_template("homeUsuario.html", rows=Listaproductos(), persona=persona)
    else:
        return render_template("login.html")

# preguntar esto
def Listaproductos(): 
    try:
        with sqlite3.connect("cafeteria.db") as con:
            # Convierte el registro en un diccionario
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM productos")
            rows = cur.fetchall()
            return rows
    except:
        return print("nose encontro")


@app.route("/buscar", methods=["POST", "GET"])
def buscarProducto():
    if "user" in session:
        persona["usuario"] = session["user"]
        if (request.method == "POST"):
            id = request.form["producto"]
            session["ref"] = id
            try:
                with sqlite3.connect("cafeteria.db") as con:
                    # Convierte el registro en un diccionario
                    con.row_factory = sqlite3.Row
                    cur = con.cursor()
                    cur.execute("SELECT * FROM productos WHERE id = ?", [id])
                    row = cur.fetchone()
                    session["cantidad"] = row["cantidad"]
                return render_template("buscarProducto.html", row=row, persona=persona)
            except:
                return render_template("buscarProducto.html", persona=persona)
        return render_template("buscarProducto.html", persona=persona)
    else:
        return render_template("login.html")


@app.route("/comprar", methods=["POST", "GET"])
def comprar():
    if "user" in session:
        persona["usuario"] = session["user"]
        if (request.method == "POST"):
            num = int(request.form["cant"])
            id = session["ref"]
            cantidad = session["cantidad"] - num
            try:
                with sqlite3.connect("cafeteria.db") as con:
                    cur = con.cursor()
                    cur.execute(
                        "UPDATE productos SET cantidad = ? WHERE id = ?", [cantidad, id])
                    con.commit
                return render_template("buscarProducto.html", persona=persona)
            except:
                return render_template("buscarProducto.html", persona=persona)
        else:
            return render_template("buscarProducto.html", persona=persona)
    else:
        return render_template("login.html")


@app.route("/configuracionUsuario", methods=["GET"])
def configuracionUsuario():
    if "user" in session:
        persona["usuario"] = session["user"]
        return render_template("configUsuario.html", persona=persona)
    else:
        return render_template("login.html")


@app.route("/restablecerUsuario", methods=["POST"])
def reestablecer_user():
    if "user" in session:
        persona["usuario"] = session["user"]
        contravieja = request.form["contravieja"]
        contra = request.form["contra"]
        contra2 = request.form["contra2"]
        nombre = session["user"]
        h = hashlib.sha256(contra.encode())
        pwd = h.hexdigest()
        j = hashlib.sha256(contravieja.encode())
        pwdj = j.hexdigest()
        with sqlite3.connect("cafeteria.db") as con:
            #con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(
                "SELECT clave FROM usuarios WHERE usuario = ?", [nombre])
            row = cur.fetchone()
            if row:
                clave = row[0]
        if pwdj == clave:
            if contra == contra2:
                with sqlite3.connect("cafeteria.db") as con:
                    cur2 = con.cursor()
                    cur2.execute("UPDATE usuarios SET clave = ? WHERE usuario = ?", [
                                 pwd, nombre])
                    con.commit()
                    return render_template("homeUsuario.html", rows=Listaproductos(), persona=persona)
            else:
                validacion = "Claves Distintas"
                # Mostrar Mensaje nueva clave no coincide
                return render_template("configUsuario.html", validacion=validacion, persona=persona)
        else:
            validacion = "Antigua clave erronea"
            return render_template("configUsuario.html", validacion=validacion, persona=persona)
            # Mostrar mensaje clave antigua equivocada

    else:
        return render_template("login.html")

# Rutas CRUD productos


@app.route("/producto/crear", methods=["POST"])
def crearProducto():
    if "user" in session:
        persona["usuario"] = session["user"]
        idProducto = request.form["id"]
        nombre = request.form["nombre"]
        precio = request.form["precio"]
        cantidad = request.form["cantidad"]
        imagen = request.files["imagen"]
        ext = imagen.filename.rsplit(".", 1)[1]
        if ext in EXT_VALIDAS:
            try:
                with sqlite3.connect("cafeteria.db") as con:
                    url = secure_filename(imagen.filename)
                    ruta = FOLDER_IMAGENES + secure_filename(imagen.filename)
                    imagen.save(ruta)
                    cur = con.cursor()
                    cur.execute("INSERT INTO productos (id,nombre,cantidad,valor,url) VALUES (?,?,?,?,?);",
                                [idProducto, nombre, cantidad, precio, url])
                    con.commit()
                texto = "Producto guardado"
                referencia= "/crudProducto"
                return render_template("confirmar.html", texto = texto, referencia = referencia )
            except:
                texto = "Error en los datos"
                referencia= "/crudProducto"
                return render_template("confirmar.html", texto = texto , referencia= "/crudProducto" )
        else:
            texto = "Archivo no válido"
            referencia= "/crudProducto"
            return render_template("confirmar.html", texto = texto, referencia = referencia)
    else:
        return render_template("login.html")


@app.route("/producto/actualizar", methods=["POST"])
def actualizarProducto():
    if "user" in session:
        persona["usuario"] = session["user"]
        idProducto = request.form["id"]
        nombre = request.form["nombre"]
        precio = request.form["precio"]
        cantidad = request.form["cantidad"]
        imagen = request.files["imagen"]
        ext = imagen.filename.rsplit(".", 1)[1]
        if ext in EXT_VALIDAS:
            try:
                with sqlite3.connect("cafeteria.db") as con:
                    url = secure_filename(imagen.filename)
                    ruta = FOLDER_IMAGENES + secure_filename(imagen.filename)
                    imagen.save(ruta)
                    cur = con.cursor()
                    cur.execute("UPDATE productos SET nombre = ?, cantidad = ?, valor = ?, url = ? WHERE id = ?",
                                [nombre, cantidad, precio, url, idProducto])
                    con.commit()
                texto = "Producto actualizado"
                referencia= "/crudProducto"
                return render_template("confirmar.html", texto = texto , referencia = referencia)
            except:
                return render_template("crudProducto.html", persona = persona )
        else:
            texto = "Tipo de archivo no válido"
            referencia= "/crudProducto"
            return render_template("confirmar.html", texto = texto , referencia = referencia)
    else:
        return render_template("login.html")


@app.route("/producto/eliminar", methods=["POST"])
def eliminarProducto():
    if "user" in session:
        persona["usuario"] = session["user"]
        idProducto = request.form["id"]
        try:
            with sqlite3.connect("cafeteria.db") as con:
                cur = con.cursor()
                cur.execute("DELETE from productos WHERE id = ?", [idProducto])
                con.commit()
            texto = "Producto eliminado"
            referencia= "/crudProducto"
            return render_template("confirmar.html", texto = texto, referencia = referencia)
        except:
            return render_template("crudProducto.html", persona = persona)
    else:
        return render_template("login.html")


@app.route("/producto/consultar", methods=["POST"])
def consultarProducto():
    if "user" in session:
        persona["usuario"] = session["user"]
        idProducto = request.form["buscar"]
        try:
            with sqlite3.connect("cafeteria.db") as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute(
                    "SELECT * FROM productos WHERE id = ?", [idProducto])
                row = cur.fetchone()
            return render_template("crudProducto.html", row=row)
        except:
            return render_template("crudProducto.html", persona = persona)
    else:
        return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
