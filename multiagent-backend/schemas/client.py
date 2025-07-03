from pydantic import BaseModel, EmailStr, Field

class Client(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    email: EmailStr
    phone: str
    enrolled_services: list[str]
    status: str  # active, inactive
    dob: str  # YYYY-MM-DD
    created_at: str
