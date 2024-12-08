from fastapi import APIRouter, Depends, Request
from requests import Session
from core.database import get_db
from dashboard.schemas import DashboardResponseModel
from dashboard.services import get_dashbaord_data

router = APIRouter(
    prefix="/api/v1/dashboard",
    tags=["Dashbaord"],
    responses={404: {"description": "Not found"}},
)

@router.get('', response_model=DashboardResponseModel)
async def get(req: Request, db: Session = Depends(get_db)):
    return await get_dashbaord_data(req, db)