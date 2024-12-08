from fastapi import APIRouter, Depends, Request
from requests import Session
from attendances.services import create_attendance, get_attendance
from core.database import get_db
from schedule.schemas import ScheduleResponseModel
from schedule.services import create_schedule, get_schedule

router = APIRouter(
    prefix="/api/v1/attendances",
    tags=["Attendances"],
    responses={404: {"description": "Not found"}},
)

@router.post('')
async def post(req: Request, db: Session = Depends(get_db)):
    return await create_attendance(req, db)

@router.get('', response_model=list[ScheduleResponseModel])
async def get(req: Request, db: Session = Depends(get_db)):
    return await get_attendance(db, await req.json())