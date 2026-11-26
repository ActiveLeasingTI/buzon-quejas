from flask import Flask
import os

from config import Config
from models import db

from datetime import datetime
from werkzeug.utils import secure_filename

from models.reporte import Reporte
from models.usuario import Usuario
from models.evidencia import Evidencia
from models.seguimiento import Seguimiento
from models.tipo_reporte import TipoReporte
from models.categoria import Categoria
from models.departamento import Departamento

from flask_login import (LoginManager, login_user, logout_user, login_required, current_user)
from flask import(render_template, request, redirect, url_for)

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# ==========================================================================
# Utilidades
# ==========================================================================

def generar_folio():
    ultimo = Reporte.query.order_by(Reporte.id.desc()).first()
    consecutivo = 1
    if ultimo:
        consecutivo = ultimo.id + 1
        fecha = datetime.now().strftime("%Y%m%d")
        return f"BQ-{fecha}-{consecutivo:04d}"


# ==========================================================================
# Login
# ==========================================================================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        password = request.form["password"]
        usuario = Usuario.query.filter_by(correo=correo).first()
        if usuario and usuario.check_password(password):
            login_user(usuario)
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Correo o contraseña incorrectos")
    return render_template("login.html")


# ==========================================================================
# Circulación
# ==========================================================================

@app.route("/nuevo-reporte")
def nuevo_reporte():
    tipos = TipoReporte.query.filter_by(activo=True).all()
    categorias = Categoria.query.filter_by(activo=True).all()
    departamentos = Departamento.query.filter_by(activo=True).all()
    return render_template("nuevo_reporte.html", tipos=tipos, categorias=categorias, departamentos=departamentos)

@app.route("/guardar-reporte", methods=["POST"])
def guardar_reporte():
    try:
        # =====================================
        # CONFIDENCIALIDAD
        # =====================================
        confidencialidad = request.form.get("confidencialidad")
        es_anonimo = (confidencialidad == "anonimo")
        # =====================================
        # GENERACIÓN DE FOLIO
        # =====================================
        ultimo = Reporte.query.order_by(Reporte.id.desc()).first()
        consecutivo = 1
        if ultimo:
            consecutivo = ultimo.id + 1
        fecha_actual = datetime.now().strftime("%Y%m%d")
        folio = (f"BQ-{fecha_actual}-{consecutivo:04d}")
        # =====================================
        # FECHA DE OCURRENCIA
        # =====================================
        fecha_ocurrencia = request.form.get("fecha_ocurrencia")
        if fecha_ocurrencia:
            fecha_ocurrencia = datetime.strptime(fecha_ocurrencia, "%Y-%m-%d").date()
        else:
            fecha_ocurrencia = None
        # =====================================
        # CREAR REPORTE
        # =====================================
        reporte = Reporte(
            folio=folio,
            anonimo=es_anonimo,
            nombre=(
                None
                if es_anonimo
                else request.form.get("nombre")),
            correo=(
                None
                if es_anonimo
                else request.form.get("correo")),
            tipo_id=request.form.get("tipo_id"),
            categoria_id=request.form.get("categoria_id"),
            departamento_id=request.form.get("departamento_id"),
            descripcion=request.form.get("descripcion"),
            frecuencia=request.form.get("frecuencia"),
            fecha_ocurrencia=fecha_ocurrencia,
            estatus="RECIBIDO",
            prioridad="MEDIA"
        )
        db.session.add(reporte)
        db.session.commit()
        # =====================================
        # GUARDAR EVIDENCIAS
        # =====================================
        carpeta_folio = os.path.join("uploads", folio)
        os.makedirs(carpeta_folio, exist_ok=True)
        archivos = request.files.getlist("evidencias")
        for archivo in archivos:
            if archivo.filename:
                nombre_archivo = secure_filename(archivo.filename)
                ruta_archivo = os.path.join(carpeta_folio, nombre_archivo)
                archivo.save(ruta_archivo)
                evidencia = Evidencia(reporte_id=reporte.id, archivo=ruta_archivo)
                db.session.add(evidencia)
        db.session.commit()
        return render_template("reporte_exitoso.html", folio=folio)
    except Exception as e:
        db.session.rollback()
        return f"""
        <h3>Error al guardar reporte</h3>
        <p>{str(e)}</p>
        """

# ==========================================================================
# Logout
# ==========================================================================

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# ==========================================================================
# Temportal
# ==========================================================================

@app.route("/dashboard")
@login_required
def dashboard():
    return f"""Bienvenido {current_user.nombre}"""

with app.app_context():
    db.create_all()

@app.route("/")
def inicio():
    return "Sistema de Buzón funcionando"

# ==========================================================================
# Usuario Temporal
# ==========================================================================

@app.route("/crear-admin")
def crear_admin():

    admin = Usuario(
        nombre="Administrador RH",
        correo="admin@empresa.com",
        rol="ADMIN"
    )

    admin.set_password("Admin123")

    db.session.add(admin)
    db.session.commit()

    return "Administrador creado"

if __name__ == "__main__":
    app.run(debug=True)