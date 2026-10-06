from models import MensajeModel


def obtener_por_sala(db, sala_id):
    return (
        db.query(MensajeModel)
        .filter(MensajeModel.sala_id == sala_id)
        .order_by(MensajeModel.id)
        .all()
    )


def insertar(db, contenido, usuario_id, sala_id):
    mensaje = MensajeModel(contenido=contenido, usuario_id=usuario_id, sala_id=sala_id)
    db.add(mensaje)
    db.commit()
    db.refresh(mensaje)
    return mensaje
