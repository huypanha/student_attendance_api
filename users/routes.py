from fastapi import APIRouter, status, Depends, Request, File, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from core.database import get_db
from users.schemas import CreateUserRequest
from users.services import create_user_account, get_user_account_by_email
from core.security import oauth2_scheme
from users.responses import UserResponse;

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

@router.post('', status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUserRequest, db: Session = Depends(get_db)):
    await create_user_account(data=data, db=db)
    payload = {"message": "User account has been succesfully created."}
    return JSONResponse(content=payload)


@router.post('/me', status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user_detail(request: Request):
    return request.user

# GET route to fetch user details by email
@router.get('/users', status_code=status.HTTP_200_OK)
async def get_user(email: str, db: Session = Depends(get_db)):
    user = await get_user_account_by_email(email=email, db=db)
    return user