from pydantic import BaseModel, EmailStr

class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class GetUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str