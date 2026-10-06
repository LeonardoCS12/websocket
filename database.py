from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

USUARIO = "root"
PASSWORD = "root"
HOST = "localhost"
PUERTO = 3306
BASE_DATOS = "chat_websocket_db"

DATABASE_URL = "sqlite:///./prueba.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
