import enum
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Rol(str, enum.Enum):
    ciudadano = "ciudadano"
    funcionario = "funcionario"


class TipoSolicitud(str, enum.Enum):
    peticion = "peticion"
    queja = "queja"
    reclamo = "reclamo"
    sugerencia = "sugerencia"


class EstadoSolicitud(str, enum.Enum):
    radicada = "radicada"
    en_tramite = "en_tramite"
    respondida = "respondida"
    cerrada = "cerrada"


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    rol: Mapped[Rol] = mapped_column(default=Rol.ciudadano)
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    solicitudes: Mapped[list["Solicitud"]] = relationship(
        back_populates="ciudadano", foreign_keys="Solicitud.ciudadano_id"
    )
    solicitudes_asignadas: Mapped[list["Solicitud"]] = relationship(
        back_populates="funcionario", foreign_keys="Solicitud.funcionario_id"
    )


class Solicitud(Base):
    __tablename__ = "solicitudes"

    id: Mapped[int] = mapped_column(primary_key=True)
    radicado: Mapped[str | None] = mapped_column(String(20), unique=True, index=True)
    tipo: Mapped[TipoSolicitud] = mapped_column()
    asunto: Mapped[str] = mapped_column(String(200))
    descripcion: Mapped[str] = mapped_column(Text)
    estado: Mapped[EstadoSolicitud] = mapped_column(default=EstadoSolicitud.radicada)
    ciudadano_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    funcionario_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id"), index=True
    )
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    ciudadano: Mapped["Usuario"] = relationship(
        back_populates="solicitudes", foreign_keys=[ciudadano_id]
    )
    funcionario: Mapped["Usuario | None"] = relationship(
        back_populates="solicitudes_asignadas", foreign_keys=[funcionario_id]
    )
    respuestas: Mapped[list["Respuesta"]] = relationship(
        back_populates="solicitud", cascade="all, delete-orphan"
    )


class Respuesta(Base):
    __tablename__ = "respuestas"

    id: Mapped[int] = mapped_column(primary_key=True)
    solicitud_id: Mapped[int] = mapped_column(ForeignKey("solicitudes.id"), index=True)
    autor_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    mensaje: Mapped[str] = mapped_column(Text)
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    solicitud: Mapped["Solicitud"] = relationship(back_populates="respuestas")
    autor: Mapped["Usuario"] = relationship()
