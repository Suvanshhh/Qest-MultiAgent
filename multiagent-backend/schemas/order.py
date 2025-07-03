from pydantic import BaseModel

class Order(BaseModel):
    id: str = Field(..., alias="_id")
    client_id: str
    service: str
    status: str  # paid, pending, cancelled
    created_at: str
    amount: float
