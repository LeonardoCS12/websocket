from models import UsuarioModel


def obtener_todos(db):
    return db.query(UsuarioModel).all()


def obtener_por_id(db, usuario_id):
    return db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()


def obtener_por_nombre(db, nombre):
    return db.query(UsuarioModel).filter(UsuarioModel.nombre == nombre).first()


def insertar(db, nombre):
    usuario = UsuarioModel(nombre=nombre)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario
