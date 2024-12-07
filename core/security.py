
import bcrypt
from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError
from core.config import get_settings
from core.database import get_db
from users.models import UserModel

settings = get_settings()

def get_password_hash(password):
    enPass = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(enPass, bcrypt.gensalt())
    return hashed_password.decode("utf-8")

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

async def create_access_token(data, expiry: timedelta):
    payload = data.copy()
    expire_in = datetime.now(timezone.utc) + expiry
    payload.update({"exp": expire_in})
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

async def sign_token(data):
    expire_in = datetime.now(timezone.utc) + timedelta(days=1)
    data.update({"exp": expire_in})
    return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

async def create_refresh_token(data):
    return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def get_token_payload(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        return None
    return payload


def get_current_user(token: str, db = None):
    payload = get_token_payload(token)
    if not payload or type(payload) is not dict:
        return None

    user_id = payload.get('id', None)
    if not user_id:
        return None

    if not db:
        db = next(get_db())

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    return user