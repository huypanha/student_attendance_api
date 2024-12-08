import json
from fastapi.responses import JSONResponse
from courses.services import get_courses, get_only_courses_by_id
from schedule.models import ScheduleModel
from schedule.schemas import ScheduleResponseModel
from fastapi.exceptions import HTTPException

async def create_schedule(req, db):
    data = dict(await req.form()).get('data', None)
    if data is None:
        raise HTTPException(status_code=500, detail="Data is empty")

    try:
        for s in json.loads(data):
            new_data = ScheduleModel(
                startTime = s['startTime'],
                endTime = s['endTime'],
                courseId = s['courseId'],
                colorCode = s['colorCode'],
                createdBy = req.state.user.id,
            )
            db.add(new_data)
        db.commit()

    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to create schedule")
    
    return JSONResponse(content="Schedule created successfully")

async def get_schedule(db, req):
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

async def update_schedule(req, db):
    data = dict(await req.form()).get('new_data', None)
    if data is None:
        raise HTTPException(status_code=500, detail="Data is empty")
    
    print(len(json.loads(data)))

    try:
        for s in json.loads(data):
            new_data = db.query(ScheduleModel).filter(ScheduleModel.id == s['id']).first()
            if new_data is not None:
                new_data.startTime = s['startTime']
                new_data.endTime = s['endTime']
                new_data.courseId = s['courseId']
                new_data.colorCode = s['colorCode']
                new_data.createdBy = req.state.user.id
                db.add(new_data)
        db.commit()

    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to update schedule")
    
    return JSONResponse(content="Schedule updated successfully")

async def delete_schedule(req, db):
    ids = dict(await req.form()).get('ids', None)
    if ids is None:
        raise HTTPException(status_code=400, detail="id is required")

    try:
        for id in json.loads(ids):
            findData = db.query(ScheduleModel).filter(ScheduleModel.id == id).first()
            if findData is not None:
                db.delete(findData)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to delete course")
    
    return JSONResponse(content="Deleted sucessfully")