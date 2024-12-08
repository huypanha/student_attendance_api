from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from sqlalchemy import inspect

from users.responses import UserResponseModel

class CourseResponseModel(BaseModel):
    id: int
    subject: Optional[str]
    teacherId: Optional[int]
    description: Optional[str]
    img: Optional[str]
    createdBy: Optional[int]
    createdAt: Optional[datetime]
    updatedBy: Optional[int]
    updatedAt: Optional[datetime]
    status: Optional[str] = 'A'
    teacherModel: UserResponseModel = None
    students: list[UserResponseModel] = None

    model_config = ConfigDict(from_attributes=True)

def model_to_dict(instance):
    return {c.key: getattr(instance, c.key) for c in inspect(instance).mapper.column_attrs}

class StudentCourseResponseModel(BaseModel):
    stuId: int
    courseId: int
    joinDate: datetime
    createdBy: int

    model_config = ConfigDict(from_attributes=True)