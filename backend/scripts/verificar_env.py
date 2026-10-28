"""Comprueba que el .env de la raíz y backend/.env tengan las mismas credenciales, sin mostrarlas.

Uso, desde backend/ con el entorno activo:
    python -m scripts.verificar_env
"""

from pathlib import Path
from urllib.parse import urlparse

from dotenv import dotenv_values

BACKEND = Path(__file__).resolve().parent.parent
RAIZ = BACKEND.parent

raiz = dotenv_values(RAIZ / ".env")
url = urlparse(dotenv_values(BACKEND / ".env").get("DATABASE_URL") or "")
password = raiz.get("POSTGRES_PASSWORD") or ""

checks = {
    "usuario igual en los dos .env": raiz.get("POSTGRES_USER") == url.username,
    "contraseña igual en los dos .env": password == url.password,
    "base de datos igual en los dos .env": raiz.get("POSTGRES_DB") == url.path.lstrip("/"),
    "contraseña solo con letras y números": password.isalnum(),
    "contraseña distinta a la de ejemplo": password != "fakepassword",
}

for descripcion, ok in checks.items():
    print(f"{'OK   ' if ok else 'FALLA'} {descripcion}")
