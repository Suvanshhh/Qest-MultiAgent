from pydantic import BaseModel

class Course(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    instructor: str
    status: str  # ongoing, upcoming, completed
    start_date: str
    end_date: str
