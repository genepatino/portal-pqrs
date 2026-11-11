from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models import EstadoSolicitud, Rol, TipoSolicitud


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


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class SolicitudCrear(BaseModel):
    tipo: TipoSolicitud
    asunto: str = Field(min_length=5, max_length=200)
    descripcion: str = Field(min_length=10, max_length=5000)


class SolicitudRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    radicado: str
    tipo: TipoSolicitud
    asunto: str
    descripcion: str
    estado: EstadoSolicitud
    creado_en: datetime
    actualizado_en: datetime
