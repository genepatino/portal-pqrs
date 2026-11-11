from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Usuario
from app.schemas import Token, UsuarioCrear, UsuarioRespuesta
from app.security import crear_token_acceso, hashear_password, verificar_password

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


@router.post("/login", response_model=Token)
def iniciar_sesion(
    formulario: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    email = formulario.username.lower()
    usuario = db.scalar(select(Usuario).where(Usuario.email == email))

    if usuario is None or not verificar_password(formulario.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(access_token=crear_token_acceso(usuario.id))
