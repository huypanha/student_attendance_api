from fastapi import APIRouter, Depends, File, Request, UploadFile
from requests import Session
from core.database import get_db
from users.responses import UserResponseModel
from users.services import delete_user, get_users, update_user

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
    responses={404: {"description": "Unauthorized"}},
)

@router.get('', response_model=list[UserResponseModel])
async def get(request: Request, db: Session = Depends(get_db)):
    return await get_users(data=await request.json(), db=db)

@router.put('')
async def update(data: Request, profileImg: UploadFile = File(None), db: Session = Depends(get_db)):
    return await update_user(data, profileImg, db)

@router.delete('')
async def delete(data: Request, db: Session = Depends(get_db)):
    return await delete_user(data, db)