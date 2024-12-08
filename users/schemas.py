from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import date, datetime

class CreateUserRequest(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str
    type: int

class UpdateUserRequest(BaseModel):
    id: int
    stuId: str
    firstName: str
    lastName: str
    email: str
    phoneNumber: str
    dob: date
    type: int
    status: str | None
    password: str | None

class GetUserRequest(BaseModel):
    type: int = None
    types: list = None

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

    model_config = ConfigDict(from_attributes=True)