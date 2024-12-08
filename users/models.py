from sqlalchemy import Column, Integer, String, DateTime, func, Date, CHAR
from core.database import Base

# User Model
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stuId = Column(String(255))
    firstName = Column(String(255))
    lastName = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    phoneNumber = Column(String(20))
    dob = Column(Date)
    type = Column(Integer) # 0: for teacher, 1: for student
    createdBy = Column(Integer)
    updatedBy = Column(Integer)
    createdAt = Column(DateTime, default=func.now()) 
    updatedAt = Column(DateTime)
    lastActive = Column(DateTime, default=func.now()) 
    status = Column(CHAR(1), default='A')