from sqlalchemy import CHAR, TIMESTAMP, Column, ForeignKey, Integer, PrimaryKeyConstraint, String, Text, func
from core.database import Base
from sqlalchemy.orm import relationship

class CourseModel(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(255))
    teacherId = Column(Integer)
    description = Column(Text)
    img = Column(String(255))
    createdBy = Column(Integer)
    createdAt = Column(TIMESTAMP, default=func.now()) 
    updatedBy = Column(Integer)
    updatedAt = Column(TIMESTAMP)
    status = Column(CHAR(1), default='A')

    __table_args__ = (
        PrimaryKeyConstraint('id'),
    )

class StudentCourseModel(Base):
    __tablename__ = "student_course"

    stuId = Column(Integer, nullable=False)
    courseId = Column(Integer, nullable=False)
    joinDate = Column(TIMESTAMP, nullable=False, default=func.now()) 
    createdBy = Column(Integer, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('stuId', 'courseId'),
    )