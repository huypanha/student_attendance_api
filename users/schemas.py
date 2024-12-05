from pydantic import BaseModel, EmailStr

class CreateUserRequest(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str
    type: int

class GetUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

from pydantic import BaseModel
from datetime import date, datetime

class UserResponse(BaseModel):
    id: int
    stuId: str | None
    firstName: str
    lastName: str
    email: str
    phoneNumber: str | None
    dob: date | None
    type: int
    createdBy: int | None
    updatedBy: int | None
    createdAt: datetime
    updatedAt: datetime | None
    lastActive: datetime
    status: str

    class Config:
        orm_mode = True
        from_attributes = True