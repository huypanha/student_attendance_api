import os
from pathlib import Path
import shutil
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from sqlalchemy import and_, func
from users.models import UserModel
from fastapi.exceptions import HTTPException
from core.security import get_password_hash
from datetime import datetime

from users.schemas import UpdateUserRequest

env = Path(".") / ".env"
load_dotenv(dotenv_path=env)

async def create_user_account(data, db):
    user = db.query(UserModel).filter(UserModel.email == data.email).first()
    if user:
        raise HTTPException(status_code=422, detail="Email is already registered with us.")

    new_user = UserModel(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        password=get_password_hash(data.password),
        is_active=False,
        is_verified=False,
        registered_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Function to get user data by email
async def get_user_account_by_email(email: str, db):
    user = db.query(UserModel).filter(UserModel.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    return user

async def get_users(data, db):
    getUser = db.query(UserModel)

    if data.get('id', None) is not None:
        getUser = getUser.filter(UserModel.id == data.get('id', None))

    if data.get('type', None) is not None:
        getUser = getUser.filter(UserModel.type == data.get('type', None))

    if data.get('status', None) is not None:
        getUser = getUser.filter(UserModel.status == data.get('status', None))

    getUser.order_by(UserModel.id.desc()).all()

    return getUser

async def update_user(req, profileImg, db):
    user = UpdateUserRequest.model_validate(dict(await req.form()))
    
    checkUser = db.query(UserModel).filter(and_(UserModel.email == user.email, UserModel.id != user.id)).first()
    if checkUser:
        raise HTTPException(status_code=422, detail="This email address is already registered")
    
    new_user = db.query(UserModel).filter(UserModel.id == user.id).first()
    new_user.stuId = user.stuId
    new_user.firstName = user.firstName
    new_user.lastName = user.lastName
    new_user.email = user.email
    new_user.phoneNumber = user.phoneNumber
    new_user.dob = user.dob
    new_user.updatedAt = func.now()
    new_user.updatedBy = req.state.user.id

    if user.password is not None:
        new_user.password = get_password_hash(user.password)

    try:
        db.add(new_user)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to update user info")
    
    if profileImg is not None:
        Path(os.getenv('USER_PROFILE_PATH')).mkdir(parents=True, exist_ok=True)
        path = Path(os.getenv('USER_PROFILE_PATH')) / f"{new_user.id}.png"
        with path.open("wb") as buffer:
            shutil.copyfileobj(profileImg.file, buffer)
    
    return JSONResponse(content="Updated sucessfully")

async def delete_user(req, db):
    id = dict(await req.form()).get('id')
    if id is None:
        raise HTTPException(status_code=400, detail="id is required")
    
    checkUser = db.query(UserModel).filter(UserModel.id == id).first()
    if not checkUser:
        raise HTTPException(status_code=422, detail="Not found")
    
    checkUser.status = 'D'

    try:
        db.add(checkUser)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to delete user")
    
    return JSONResponse(content="Deleted sucessfully")