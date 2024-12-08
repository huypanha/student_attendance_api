from pydantic import BaseModel, ConfigDict
from datetime import datetime

from courses.responses import CourseResponseModel

class ScheduleResponseModel(BaseModel):
    id: int
    startTime: datetime
    endTime: datetime
    courseId: int
    courseModel: CourseResponseModel
    colorCode: str
    createdBy: int
    createdDate: datetime

    model_config = ConfigDict(from_attributes=True)