import logging

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from repositories import mensaje_repository
from services import sala_service

logger = logging.getLogger("chat_websocket")


def _error_bd(db, e):
    db.rollback()
    logger.error("Error de conexion con la base de datos: %s", e)
    return HTTPException(status_code=500, detail="Error al acceder a la base de datos")


def crear_mensaje(db, contenido, usuario_id, sala_id):
    if not isinstance(contenido, str) or not contenido.strip():
        logger.error("El contenido del mensaje esta vacio")
        raise HTTPException(status_code=400, detail="El contenido del mensaje no puede estar vacío")
    try:
        return mensaje_repository.insertar(db, contenido, usuario_id, sala_id)
    except SQLAlchemyError as e:
        raise _error_bd(db, e)


def historial_sala(db, sala_id):
    sala_service.obtener_sala(db, sala_id)
    try:
        return mensaje_repository.obtener_por_sala(db, sala_id)
    except SQLAlchemyError as e:
        raise _error_bd(db, e)
