from typing import Dict, List

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.salas: Dict[int, List[WebSocket]] = {}

    async def conectar(self, websocket: WebSocket, sala_id: int):
        await websocket.accept()
        if sala_id not in self.salas:
            self.salas[sala_id] = []
        self.salas[sala_id].append(websocket)

    async def rechazar(self, websocket: WebSocket):
        await websocket.close(code=1008)

    def desconectar(self, websocket: WebSocket, sala_id: int):
        if sala_id in self.salas and websocket in self.salas[sala_id]:
            self.salas[sala_id].remove(websocket)
            if not self.salas[sala_id]:
                del self.salas[sala_id]

    async def difundir(self, mensaje: dict, sala_id: int):
        for conexion in list(self.salas.get(sala_id, [])):
            try:
                await conexion.send_json(mensaje)
            except Exception:
                self.desconectar(conexion, sala_id)


manager = ConnectionManager()
