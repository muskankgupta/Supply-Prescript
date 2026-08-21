from fastapi import FastAPI

from backend.routes.shipments import router as shipments_router
from backend.routes.predictions import router as predictions_router
from backend.routes.recommendations import router as recommendations_router

app = FastAPI(
    title="Supply Prescript API",
    version="1.0.0",
)


app.include_router(shipments_router)
app.include_router(predictions_router)
app.include_router(recommendations_router)


@app.get("/")
def root():
    return {
        "message": "Supply Prescript API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "database": "PostgreSQL",
    }