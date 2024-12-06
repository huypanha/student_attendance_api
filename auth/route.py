from fastapi import APIRouter, status, Depends, Header, File, UploadFile, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.database import get_db
from auth.services import get_token, get_refresh_token, login, register_user
from users.responses import UserResponse
from users.schemas import CreateUserRequest

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)

@router.post("/token", status_code=status.HTTP_200_OK)
async def authenticate_user(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await get_token(data=data, db=db)

@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_access_token(refresh_token: str = Header(), db: Session = Depends(get_db)):
    return await get_refresh_token(token=refresh_token, db=db)

@router.post("/register", status_code=status.HTTP_200_OK)
async def register(data: Request, profileImg: UploadFile = File(None), db: Session = Depends(get_db)):
    user = CreateUserRequest.model_validate(dict(await data.form()))
    return await register_user(user, profileImg, db)

@router.post("/login", status_code=status.HTTP_200_OK)
async def register(token: Request, db: Session = Depends(get_db)):
    return await login(dict(await token.form()).get('token'), db)