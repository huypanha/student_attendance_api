from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, String, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ScheduleModel(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True, index=True)
    startTime = Column(TIMESTAMP, nullable=False)
    endTime = Column(TIMESTAMP, nullable=False)
    courseId = Column(Integer, nullable=False)
    colorCode = Column(String(10), nullable=False)
    createdBy = Column(Integer, nullable=False)
    createdDate = Column(TIMESTAMP, nullable=False, default=func.now()) 