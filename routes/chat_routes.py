import logging

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from connection_manager import manager
from database import SessionLocal
from services import mensaje_service, sala_service, usuario_service

router = APIRouter()
logger = logging.getLogger("chat_websocket")


@router.websocket("/ws/{sala_id}/{usuario_id}")
async def chat_endpoint(websocket: WebSocket, sala_id: int, usuario_id: int):
    db = SessionLocal()
    try:
        usuario = usuario_service.obtener_usuario(db, usuario_id)
        sala_service.obtener_sala(db, sala_id)
        nombre = usuario.nombre
    except HTTPException:
        await manager.rechazar(websocket)
        return
    finally:
        db.close()

    await manager.conectar(websocket, sala_id)
    logger.info("Usuario '%s' conectado a la sala %s", nombre, sala_id)
    await manager.difundir(
        {"tipo": "sistema", "mensaje": f"{nombre} se ha unido a la sala"}, sala_id
    )

    try:
        while True:
            data = await websocket.receive_json()
            db = SessionLocal()
            try:
                mensaje = mensaje_service.crear_mensaje(
                    db, data.get("contenido"), usuario_id, sala_id
                )
                respuesta = {
                    "usuario": nombre,
                    "contenido": mensaje.contenido,
                    "fecha_envio": mensaje.fecha_envio.isoformat(),
                }
            except HTTPException as e:
                await websocket.send_json({"tipo": "error", "mensaje": e.detail})
                continue
            finally:
                db.close()
            logger.info("Mensaje enviado por usuario %s en sala %s", usuario_id, sala_id)
            await manager.difundir(respuesta, sala_id)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.error("Error en la conexion WebSocket: %s", e)

    manager.desconectar(websocket, sala_id)
    logger.info("Usuario '%s' desconectado de la sala %s", nombre, sala_id)
    await manager.difundir(
        {"tipo": "sistema", "mensaje": f"{nombre} ha salido de la sala"}, sala_id
    )
