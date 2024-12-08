from fastapi.responses import JSONResponse
from sqlalchemy import func
from attendances.models import AttendanceModel
from courses.services import get_courses
from schedule.models import ScheduleModel
from schedule.schemas import ScheduleResponseModel
from fastapi.exceptions import HTTPException

async def create_attendance(req, db):
    data = dict(await req.form())

    try:
        new_data = AttendanceModel(
            stuId = req.state.user.id,
            courseId = data['courseId'],
            type = data['type']
        )
        db.add(new_data)
        db.commit()

    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to create attendance")
    
    return JSONResponse(content="Attendance created successfully")

async def get_attendance(db, req):
    getData = db.query(ScheduleModel).all()

    results = []
    for s in getData:
        c = (await get_courses(db, {
            "id": s.courseId,
        }))[0]
        
        updated_data = ScheduleResponseModel(
            id = s.id,
            startTime = s.startTime,
            endTime = s.endTime,
            courseId = s.courseId,
            courseModel = c,
            colorCode = s.colorCode,
            createdBy = s.createdBy,
            createdDate = s.createdDate,
        )
        results.append(updated_data)

    return results