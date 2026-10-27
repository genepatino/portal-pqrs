from fastapi import FastAPI

app = FastAPI(title="Portal PQRS API")


@app.get("/health")
def health():
    return {"status": "ok"}