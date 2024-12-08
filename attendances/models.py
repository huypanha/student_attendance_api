from sqlalchemy import Column, Integer, TIMESTAMP, SmallInteger, func
from core.database import Base

class AttendanceModel(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    stuId = Column(Integer, nullable=False)
    courseId = Column(Integer, nullable=False)
    createdAt = Column(TIMESTAMP, nullable=False, default=func.now()) 
    type = Column(SmallInteger, nullable=False)