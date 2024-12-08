from typing import Optional
from pydantic import BaseModel, ConfigDict
from attendances.schemas import AttendanceResponseModel
from courses.responses import CourseResponseModel

class DashboardResponseModel(BaseModel):
    course: Optional[CourseResponseModel] = None
    attendances: Optional[list[AttendanceResponseModel]] = None

    model_config = ConfigDict(from_attributes=True)