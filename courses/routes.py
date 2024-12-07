from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from core.database import get_db
from courses.models import CourseModel
from users.schemas import CreateUserRequest
from users.services import create_user_account, get_user_account_by_email
from users.responses import UserResponse;

router = APIRouter(
    prefix="/api/v1/courses",
    tags=["Courses"],
    responses={404: {"description": "Not found"}},
)

router.get("/courses/{course_id}")
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

router.post("/")
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = CourseModel(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

router.put("/courses/{course_id}")
def update_course(course_id: int, course_update: CourseUpdate, db: Session = Depends(get_db)):
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    for key, value in course_update.dict(exclude_unset=True).items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course