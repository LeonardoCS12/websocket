import logging

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from repositories import usuario_repository

logger = logging.getLogger("chat_websocket")


def _error_bd(db, e):
    db.rollback()
    logger.error("Error de conexion con la base de datos: %s", e)
    return HTTPException(status_code=500, detail="Error al acceder a la base de datos")


def crear_usuario(db, nombre):
    if not nombre.strip():
        raise HTTPException(status_code=400, detail="El nombre del usuario no puede estar vacío")
    try:
        if usuario_repository.obtener_por_nombre(db, nombre):
            logger.error("El nombre de usuario ya existe")
            raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
        usuario = usuario_repository.insertar(db, nombre)
        logger.info("Usuario '%s' creado con id %s", usuario.nombre, usuario.id)
        return usuario
    except SQLAlchemyError as e:
        raise _error_bd(db, e)


def listar_usuarios(db):
    try:
        return usuario_repository.obtener_todos(db)
    except SQLAlchemyError as e:
        raise _error_bd(db, e)


def obtener_usuario(db, usuario_id):
    try:
        usuario = usuario_repository.obtener_por_id(db, usuario_id)
    except SQLAlchemyError as e:
        raise _error_bd(db, e)
    if usuario is None:
        logger.error("Usuario no encontrado")
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario
