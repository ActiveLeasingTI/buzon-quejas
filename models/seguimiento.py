from models import db


class Seguimiento(db.Model):

    __tablename__ = "seguimiento"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    reporte_id = db.Column(
        db.Integer,
        db.ForeignKey("reportes.id"),
        nullable=False
    )

    responsable = db.Column(
        db.String(200)
    )

    comentario = db.Column(
        db.Text
    )

    estatus = db.Column(
        db.String(50)
    )

    fecha_movimiento = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )