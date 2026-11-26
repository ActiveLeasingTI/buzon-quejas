from models import db


class Evidencia(db.Model):

    __tablename__ = "evidencias"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    reporte_id = db.Column(
        db.Integer,
        db.ForeignKey("reportes.id"),
        nullable=False
    )

    archivo = db.Column(
        db.String(255),
        nullable=False
    )

    fecha_subida = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )