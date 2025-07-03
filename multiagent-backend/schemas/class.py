from pydantic import BaseModel

class Class(BaseModel):
    id: str = Field(..., alias="_id")
    course_id: str
    date: str
    instructor: str
    status: str  # scheduled, completed
