from pydantic import BaseModel, ConfigDict
from datetime import datetime

class AttendanceResponseModel(BaseModel):
    id: int
    stuId: int
    courseId: int
    createdAt: datetime
    type: int

    model_config = ConfigDict(from_attributes=True)