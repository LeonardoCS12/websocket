from models import SalaModel


def obtener_todas(db):
    return db.query(SalaModel).all()


def obtener_por_id(db, sala_id):
    return db.query(SalaModel).filter(SalaModel.id == sala_id).first()


def insertar(db, nombre, descripcion):
    sala = SalaModel(nombre=nombre, descripcion=descripcion)
    db.add(sala)
    db.commit()
    db.refresh(sala)
    return sala
