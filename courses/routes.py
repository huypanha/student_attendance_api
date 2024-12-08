from fastapi import APIRouter, Depends, File, Request, UploadFile
from requests import Session
from core.database import get_db
from courses.responses import CourseResponseModel
from courses.services import create_course, delete_course, get_courses, update_course

router = APIRouter(
    prefix="/api/v1/courses",
    tags=["Courses"],
    responses={404: {"description": "Not found"}},
)

@router.post('', response_model=CourseResponseModel)
async def post(request: Request, imgFile: UploadFile = File(None), db: Session = Depends(get_db)):
    return await create_course(request, imgFile, db)

@router.get('', response_model=list[CourseResponseModel])
async def get(request: Request, db: Session = Depends(get_db)):
    return await get_courses(db, data=await request.json())

@router.put('', response_model=CourseResponseModel)
async def update(req: Request, imgFile: UploadFile = File(None), db: Session = Depends(get_db)):
    return await update_course(req, imgFile, db)

@router.delete('')
async def delete(data: Request, db: Session = Depends(get_db)):
    return await delete_course(data, db)