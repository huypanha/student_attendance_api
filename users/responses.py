from pydantic import BaseModel, EmailStr
from typing import Optional, Union
from datetime import date, datetime

class BaseResponse(BaseModel):
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class UserResponseModel(BaseModel):
    id: int
    stuId: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[EmailStr] = None
    phoneNumber: Optional[str] = None
    dob: Optional[date] = None
    type: Optional[int] = None
    createdBy: Optional[int] = None
    updatedBy: Optional[int] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    lastActive: Optional[datetime] = None
    status: Optional[str] = 'A'

    class Config:
        orm_mode = True