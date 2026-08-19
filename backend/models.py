from pydantic import BaseModel
from typing import Optional


class DecisionCreate(BaseModel):
    shipment_id: str
    recommendation_id: Optional[str] = None
    selected_action: str
    predicted_cost: Optional[float] = None
    predicted_delay: Optional[int] = None
    decision_status: str = "SELECTED"