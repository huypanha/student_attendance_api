from pydantic import BaseModel, EmailStr
from typing import Union
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    firstName: str
    lastName: str
    email: EmailStr
    createdAt: Union[None, datetime] = None