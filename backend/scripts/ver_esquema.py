"""Muestra el SQL que SQLAlchemy generaría para los modelos, sin conectarse a la base de datos.

Uso, desde backend/ con el entorno activo:
    python -m scripts.ver_esquema
"""

from sqlalchemy import inspect
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import configure_mappers
from sqlalchemy.schema import CreateIndex, CreateTable

from app import models  # noqa: F401  (importarlo registra los modelos en Base)
from app.database import Base

# Valida las relaciones: si hay un error en un relationship, falla aquí.
configure_mappers()

dialecto = postgresql.dialect()

for tabla in Base.metadata.sorted_tables:
    print(CreateTable(tabla).compile(dialect=dialecto))
    for indice in tabla.indexes:
        print(f"{CreateIndex(indice).compile(dialect=dialecto)};")
    print()

print("-- Relaciones")
for mapper in Base.registry.mappers:
    for rel in inspect(mapper).relationships:
        destino = rel.mapper.class_.__name__
        tipo = "lista" if rel.uselist else "uno"
        print(f"-- {mapper.class_.__name__}.{rel.key} -> {destino} ({tipo})")
