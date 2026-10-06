import logging

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from repositories import sala_repository

logger = logging.getLogger("chat_websocket")


def _error_bd(db, e):
    db.rollback()
    logger.error("Error de conexion con la base de datos: %s", e)
    return HTTPException(status_code=500, detail="Error al acceder a la base de datos")


def crear_sala(db, nombre, descripcion):
    if not nombre.strip():
        raise HTTPException(status_code=400, detail="El nombre de la sala no puede estar vacío")
    try:
        sala = sala_repository.insertar(db, nombre, descripcion)
        logger.info("Sala '%s' creada con id %s", sala.nombre, sala.id)
        return sala
    except SQLAlchemyError as e:
        raise _error_bd(db, e)


def listar_salas(db):
    try:
        return sala_repository.obtener_todas(db)
    except SQLAlchemyError as e:
        raise _error_bd(db, e)


def obtener_sala(db, sala_id):
    try:
        sala = sala_repository.obtener_por_id(db, sala_id)
    except SQLAlchemyError as e:
        raise _error_bd(db, e)
    if sala is None:
        logger.error("Sala no encontrada")
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    return sala
