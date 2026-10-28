"""Se conecta a PostgreSQL con el engine de app/database.py y muestra a qué se conectó.

Uso, desde backend/ con el entorno activo y la base de datos levantada:
    python -m scripts.probar_conexion
"""

from sqlalchemy import text

from app.database import engine

with engine.connect() as conn:
    version = conn.execute(text("select version()")).scalar()
    usuario = conn.execute(text("select current_user")).scalar()
    base = conn.execute(text("select current_database()")).scalar()

print(version)
print(f"usuario: {usuario} | base: {base}")
