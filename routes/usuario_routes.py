from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import UsuarioCreate, UsuarioResponse
from services import usuario_service

router = APIRouter()


@router.post("/usuarios", response_model=UsuarioResponse, status_code=201)
def crear_usuario(datos: UsuarioCreate, db: Session = Depends(get_db)):
    return usuario_service.crear_usuario(db, datos.nombre)


@router.get("/usuarios", response_model=List[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return usuario_service.listar_usuarios(db)
