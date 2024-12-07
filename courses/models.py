from sqlalchemy import CHAR, TIMESTAMP, Column, Integer, String, Text
from core.database import Base

class CourseModel(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(255))
    teacherId = Column(Integer)
    description = Column(Text)
    img = Column(String(255))
    createdBy = Column(Integer)
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(Integer)
    updatedAt = Column(TIMESTAMP)
    status = Column(CHAR(1))