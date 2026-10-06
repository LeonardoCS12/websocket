# Practica: Chat en tiempo real con WebSockets y FastAPI

## Ejecucion
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
1. Ejecutar `schema.sql` en MySQL.
2. Editar `database.py` y poner la contrasena de MySQL.
3. `uvicorn main:app --reload`
4. Documentacion REST: http://localhost:8000/docs
5. Cliente de chat: http://localhost:8000/static/index.html

## Arquitectura

## Diferencias entre HTTP y WebSocket
