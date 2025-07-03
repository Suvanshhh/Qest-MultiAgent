from pydantic import BaseModel

class Attendance(BaseModel):
    id: str = Field(..., alias="_id")
    class_id: str
    client_id: str
    attended: bool
