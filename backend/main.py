from fastapi import FastAPI, HTTPException
from backend.models import DecisionRequest, DecisionResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.shipments import router as shipments_router
from backend.routes.predictions import router as predictions_router
from backend.routes.recommendations import router as recommendations_router
from backend.routes.decisions import router as decisions_router


app = FastAPI(
    title="Supply Prescript API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(shipments_router)
app.include_router(predictions_router)
app.include_router(recommendations_router)
app.include_router(decisions_router)


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
@app.post("/decisions", response_model=DecisionResponse)
def execute_decision(request: DecisionRequest):

    try:
        return DecisionResponse(
            status="success",
            message="Decision executed successfully",
            shipment_id=request.shipment_id,
            recommendation_id=request.recommendation_id,
            selected_action=request.selected_action,
            predicted_cost=request.predicted_cost,
            predicted_delay=request.predicted_delay,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to execute decision: {str(exc)}"
        )