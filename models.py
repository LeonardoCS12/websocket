from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func

from database import Base


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)
    fecha_registro = Column(DateTime, server_default=func.now())


class SalaModel(Base):
    __tablename__ = "salas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)


class MensajeModel(Base):
    __tablename__ = "mensajes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    contenido = Column(Text, nullable=False)
    fecha_envio = Column(DateTime, server_default=func.now())
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    sala_id = Column(Integer, ForeignKey("salas.id"), nullable=False)
