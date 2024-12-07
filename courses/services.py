from users.models import UserModel
from fastapi.exceptions import HTTPException
from core.security import get_password_hash
from datetime import datetime


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
    # Query the user model
    user = db.query(UserModel).filter(UserModel.email == email).first()

    # If the user is not found, raise a 404 error
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    # Return the user object if found
    return user
