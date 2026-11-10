from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models import Rol


class UsuarioCrear(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UsuarioRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    email: EmailStr
    rol: Rol
    creado_en: datetime
