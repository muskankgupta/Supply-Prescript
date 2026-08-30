from pydantic import BaseModel, Field
from typing import Optional


class DecisionCreate(BaseModel):
    shipment_id: str
    recommendation_id: Optional[str] = None
    selected_action: str
    predicted_cost: Optional[float] = None
    predicted_delay: Optional[int] = None
    decision_status: str = "SELECTED"


class DecisionRequest(BaseModel):
    shipment_id: str = Field(..., min_length=1)
    recommendation_id: str = Field(..., min_length=1)
    selected_action: str = Field(..., min_length=1)
    predicted_cost: float = 0.0
    predicted_delay: float = 0.0


class DecisionResponse(BaseModel):
    status: str
    message: str
    shipment_id: str
    recommendation_id: str
    selected_action: str
    predicted_cost: float
    predicted_delay: float

class FeedbackCreate(BaseModel):
    decision_id: str
    outcome: str
    actual_cost: Optional[float] = None
    actual_delay: Optional[float] = None
    success: bool
    feedback_note: Optional[str] = None


class FeedbackResponse(BaseModel):
    feedback_id: int
    decision_id: int
    outcome: str
    actual_cost: Optional[float] = None
    actual_delay: Optional[float] = None
    success: bool
    feedback_note: Optional[str] = None
class OutcomeEvaluationCreate(BaseModel):
    decision_id: str
    predicted_cost: float
    actual_cost: float
    cost_difference: float
    predicted_delay: int
    actual_delay: int
    delay_difference: int
    success: bool
    evaluation_note: str