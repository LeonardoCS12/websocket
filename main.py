import logging
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes import chat_routes, sala_routes, usuario_routes

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("chat_websocket")
logger.info("Aplicacion iniciada")

app = FastAPI()
app.include_router(usuario_routes.router)
app.include_router(sala_routes.router)
app.include_router(chat_routes.router)
app.mount("/static", StaticFiles(directory="static"), name="static")
