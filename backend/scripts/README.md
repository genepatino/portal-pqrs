# Scripts de desarrollo

Herramientas para revisar el proyecto mientras se desarrolla. No forman parte de la API.

Los scripts de Python se corren desde `backend/` con el entorno activo (`source .venv/bin/activate`) y con `-m`, para que Python encuentre el paquete `app`.

| Comando | Qué hace | Necesita la base de datos |
|---|---|---|
| `bash scripts/levantar_db.sh` | Levanta PostgreSQL y espera a que esté `healthy`. | — |
| `python -m scripts.verificar_env` | Compara las credenciales del `.env` de la raíz con `backend/.env`, sin mostrarlas. | No |
| `python -m scripts.probar_conexion` | Se conecta con el `engine` de `app/database.py` y muestra versión, usuario y base. | Sí |
| `python -m scripts.ver_esquema` | Muestra el SQL que generan los modelos y lista sus relaciones. | No |

## Orden para revisar que todo funciona

```bash
cd backend
source .venv/bin/activate
python -m scripts.verificar_env     # 1. las credenciales coinciden
bash scripts/levantar_db.sh         # 2. PostgreSQL está arriba y healthy
python -m scripts.probar_conexion   # 3. la API puede conectarse
python -m scripts.ver_esquema       # 4. los modelos no tienen errores
```

## Comandos de Docker Compose

Desde la raíz del repositorio:

```bash
docker compose up -d db                # crear y levantar el contenedor en segundo plano
docker compose ps                      # estado del contenedor
docker compose logs -f db              # logs en vivo (Ctrl+C para salir)
docker compose stop                    # apagar sin borrar
docker compose start                   # volver a encender
docker compose down                    # borrar el contenedor (los datos quedan en el volumen pgdata)
docker compose exec db psql -U pqrs_user -d pqrs_db   # consola de PostgreSQL
docker inspect -f '{{.State.Health.Status}}' pqrs-db  # solo el estado del healthcheck
docker compose --env-file .env.example config --quiet # validar la sintaxis del compose
```

Dentro de `psql`: `\dt` lista las tablas, `\d nombre_tabla` muestra su estructura y `\q` sale.

**Cuidado:** `docker compose down -v` borra también el volumen, es decir, todos los datos.
