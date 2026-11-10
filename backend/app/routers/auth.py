from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Usuario
from app.schemas import UsuarioCrear, UsuarioRespuesta
from app.security import hashear_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/registro",
    response_model=UsuarioRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def registrar_usuario(datos: UsuarioCrear, db: Annotated[Session, Depends(get_db)]):
    email = datos.email.lower()

    existente = db.scalar(select(Usuario).where(Usuario.email == email))
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con ese email",
        )

    usuario = Usuario(
        nombre=datos.nombre,
        email=email,
        password_hash=hashear_password(datos.password),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario
