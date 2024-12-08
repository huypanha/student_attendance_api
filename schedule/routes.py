from fastapi import APIRouter, Depends, Request
from requests import Session
from core.database import get_db
from courses.responses import CourseResponseModel
from schedule.schemas import ScheduleResponseModel
from schedule.services import create_schedule, delete_schedule, get_schedule, update_schedule

router = APIRouter(
    prefix="/api/v1/schedule",
    tags=["Schedule"],
    responses={404: {"description": "Not found"}},
)

@router.post('')
async def post(req: Request, db: Session = Depends(get_db)):
    return await create_schedule(req, db)

@router.get('', response_model=list[ScheduleResponseModel])
async def get(request: Request, db: Session = Depends(get_db)):
    return await get_schedule(db, await request.json())

@router.put('', response_model=CourseResponseModel)
async def update(req: Request, db: Session = Depends(get_db)):
    return await update_schedule(req, db)

@router.delete('')
async def delete(data: Request, db: Session = Depends(get_db)):
    return await delete_schedule(data, db)