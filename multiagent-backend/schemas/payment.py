from pydantic import BaseModel

class Payment(BaseModel):
    id: str = Field(..., alias="_id")
    order_id: str
    amount: float
    status: str  # paid, failed, pending
    paid_at: str
