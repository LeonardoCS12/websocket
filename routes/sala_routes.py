from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import MensajeResponse, SalaCreate, SalaResponse
from services import mensaje_service, sala_service

router = APIRouter()


@router.post("/salas", response_model=SalaResponse, status_code=201)
def crear_sala(datos: SalaCreate, db: Session = Depends(get_db)):
    return sala_service.crear_sala(db, datos.nombre, datos.descripcion)


@router.get("/salas", response_model=List[SalaResponse])
def listar_salas(db: Session = Depends(get_db)):
    return sala_service.listar_salas(db)


@router.get("/salas/{id}/mensajes", response_model=List[MensajeResponse])
def historial_mensajes(id: int, db: Session = Depends(get_db)):
    return mensaje_service.historial_sala(db, id)
