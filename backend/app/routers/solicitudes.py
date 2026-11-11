from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_usuario_actual
from app.models import Solicitud, Usuario
from app.schemas import SolicitudCrear, SolicitudRespuesta

router = APIRouter(prefix="/solicitudes", tags=["solicitudes"])


@router.post(
    "",
    response_model=SolicitudRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def crear_solicitud(
    datos: SolicitudCrear,
    usuario: Annotated[Usuario, Depends(get_usuario_actual)],
    db: Annotated[Session, Depends(get_db)],
):
    solicitud = Solicitud(
        tipo=datos.tipo,
        asunto=datos.asunto,
        descripcion=datos.descripcion,
        ciudadano_id=usuario.id,
    )
    db.add(solicitud)
    db.flush()

    año = datetime.now(timezone.utc).year
    solicitud.radicado = f"PQRS-{año}-{solicitud.id:06d}"

    db.commit()
    db.refresh(solicitud)
    return solicitud


@router.get("", response_model=list[SolicitudRespuesta])
def listar_mis_solicitudes(
    usuario: Annotated[Usuario, Depends(get_usuario_actual)],
    db: Annotated[Session, Depends(get_db)],
):
    consulta = (
        select(Solicitud)
        .where(Solicitud.ciudadano_id == usuario.id)
        .order_by(Solicitud.creado_en.desc())
    )
    return db.scalars(consulta).all()
