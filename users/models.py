from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from core.database import Base


# User Model
class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)  # Adjusted to be False by default
    verified_at = Column(DateTime, nullable=False, server_default=func.now())  # Set as not nullable with default
    registered_at = Column(DateTime, nullable=True, default=None)
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, nullable=False, server_default=func.now())
