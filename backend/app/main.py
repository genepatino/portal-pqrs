from fastapi import FastAPI

from app.routers import auth, solicitudes

app = FastAPI(title="Portal PQRS API")

app.include_router(auth.router)
app.include_router(solicitudes.router)


@app.get("/health")
def health():
    return {"status": "ok"}