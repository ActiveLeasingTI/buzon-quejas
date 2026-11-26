from models import db


class Reporte(db.Model):

    __tablename__ = "reportes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    folio = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    nombre = db.Column(
        db.String(200)
    )

    correo = db.Column(
        db.String(255)
    )

    anonimo = db.Column(
        db.Boolean,
        default=True
    )

    # =========================
    # Catálogos
    # =========================

    tipo_id = db.Column(
        db.Integer,
        db.ForeignKey("tipo_reporte.id"),
        nullable=False
    )

    categoria_id = db.Column(
        db.Integer,
        db.ForeignKey("categorias.id"),
        nullable=False
    )

    departamento_id = db.Column(
        db.Integer,
        db.ForeignKey("departamentos.id")
    )

    # =========================
    # Información del reporte
    # =========================

    descripcion = db.Column(
        db.Text,
        nullable=False
    )

    fecha_ocurrencia = db.Column(
        db.Date
    )

    frecuencia = db.Column(
        db.String(50)
    )

    propuesta_solucion = db.Column(
        db.Text
    )

    apoyo_rh = db.Column(
        db.Text
    )

    ocurrio_antes = db.Column(
        db.String(20)
    )

    reportado_previamente = db.Column(
        db.Boolean,
        default=False
    )

    reportado_a = db.Column(
        db.String(200)
    )

    autoriza_contacto = db.Column(
        db.Boolean,
        default=False
    )

    # =========================
    # Control RH
    # =========================

    estatus = db.Column(
        db.String(50),
        default="RECIBIDO"
    )

    prioridad = db.Column(
        db.String(20),
        default="MEDIA"
    )

    responsable_rh = db.Column(
        db.String(200)
    )

    fecha_cierre = db.Column(
        db.DateTime
    )

    fecha_registro = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # =========================
    # Relaciones Catálogos
    # =========================

    tipo = db.relationship(
        "TipoReporte",
        backref="reportes"
    )

    categoria = db.relationship(
        "Categoria",
        backref="reportes"
    )

    departamento = db.relationship(
        "Departamento",
        backref="reportes"
    )

    # =========================
    # Relaciones Operativas
    # =========================

    evidencias = db.relationship(
        "Evidencia",
        backref="reporte",
        lazy=True,
        cascade="all, delete-orphan"
    )

    seguimientos = db.relationship(
        "Seguimiento",
        backref="reporte",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Reporte {self.folio}>"
        )