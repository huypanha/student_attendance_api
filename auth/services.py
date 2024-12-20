import os
from dotenv import load_dotenv
from my_utils.model_to_dict import model_to_dict
from users.models import UserModel
from fastapi.exceptions import HTTPException
from core.config import get_settings
from datetime import timedelta
from auth.responses import TokenResponse
from core.security import create_access_token, create_refresh_token, get_token_payload, sign_token, verify_password, get_password_hash
import shutil
from pathlib import Path

env = Path(".") / ".env"
load_dotenv(dotenv_path=env)

settings = get_settings()

async def get_token(data, db):
    user = db.query(UserModel).filter(UserModel.email == data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Email is not registered with us.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid Login Credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    _verify_user_access(user=user)
    
    return await _get_user_token(user=user)
    
    

async def get_refresh_token(token, db):   
    payload =  get_token_payload(token=token)
    user_id = payload.get('id', None)
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await _get_user_token(user=user, refresh_token=token)

    
    
def _verify_user_access(user: UserModel):
    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Your account is inactive. Please contact support.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_verified:
        # Trigger user account verification email
        raise HTTPException(
            status_code=400,
            detail="Your account is unverified. We have resend the account verification email.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
async def _get_user_token(user: UserModel, refresh_token = None):
    payload = {"id": user.id}
    
    access_token_expiry = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = await create_access_token(payload, access_token_expiry)
    if not refresh_token:
        refresh_token = await create_refresh_token(payload)
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=access_token_expiry.seconds  # in seconds
    )
        
async def register_user(user, profileImg, db):
    checkEmail = db.query(UserModel).filter(UserModel.email == user.email).first()
    if checkEmail:
        raise HTTPException(status_code=422, detail="This email address is already registered")
    
    new_user = UserModel(
        firstName = user.firstName,
        lastName = user.lastName,
        email = user.email,
        password = get_password_hash(user.password),
        type = user.type,
        status = 'A'
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to register")
    
    if profileImg is not None:
        Path(os.getenv('USER_PROFILE_PATH')).mkdir(parents=True, exist_ok=True)
        path = Path(os.getenv('USER_PROFILE_PATH')) / f"{new_user.id}.png"
        with path.open("wb") as buffer:
            shutil.copyfileobj(profileImg.file, buffer)

    new_user.password = None
    
    return await sign_token(model_to_dict(new_user))
        
async def login_user(token, db):
    login_info = get_token_payload(token)
    checkUser = db.query(UserModel).filter(UserModel.email == login_info['id']).first()
    if not checkUser:
        raise HTTPException(status_code=422, detail="Invalid credentials")
    
    if not verify_password(login_info['password'], checkUser.password):
        raise HTTPException(status_code=422, detail="Incorrect password")

    return await sign_token({
        'id': checkUser.id,
        'stuId': checkUser.stuId,
        'firstName': checkUser.firstName,
        'lastName': checkUser.lastName,
        'email': checkUser.email,
        'phoneNumber': checkUser.phoneNumber,
        'type': checkUser.type
    })