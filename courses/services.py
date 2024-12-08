import json
import os
from pathlib import Path
import shutil
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from sqlalchemy import func
from courses.models import CourseModel, StudentCourseModel
from courses.responses import CourseResponseModel
from fastapi.exceptions import HTTPException
from datetime import datetime

from users.services import get_users

env = Path(".") / ".env"
load_dotenv(dotenv_path=env)

async def create_course(request, imgFile, db):
    data = dict(await request.form())

    fileName = ''
    if imgFile is not None:
        Path(os.getenv('COURSE_IMG_PATH')).mkdir(parents=True, exist_ok=True)
        fileName = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        path = Path(os.getenv('COURSE_IMG_PATH')) / fileName
        with path.open("wb") as buffer:
            shutil.copyfileobj(imgFile.file, buffer)
        
    new_data = CourseModel(
        subject = data['subject'],
        teacherId = data['teacherId'],
        description = data['description'],
        img = fileName,
        createdBy = request.state.user.id
    )

    try:
        db.add(new_data)
        db.commit()
        db.refresh(new_data)

        # assign selected students to new created course
        for s in json.loads(data['studentIds']):
            sc_data = StudentCourseModel(
                stuId = s,
                courseId = new_data.id,
                createdBy = request.state.user.id
            )
            db.add(sc_data)
            db.commit()

    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to create course")
    
    return new_data

async def get_courses(db, data):
    getData = db.query(CourseModel).filter(CourseModel.status == 'A')

    if data.get('teacherId', None) is not None:
        getData = getData.filter(CourseModel.teacherId == data.get('teacherId', None))

    if data.get('id', None) is not None:
        getData = getData.filter(CourseModel.id == data['id'])

    getData.order_by(CourseModel.id.desc()).all()

    results = []
    # You can join tables
    for c in getData:
        tm = await get_users({
            "id": c.teacherId,
        }, db)
        
        updated_course = CourseResponseModel(
            id = c.id,
            subject = c.subject,
            teacherId = c.teacherId,
            description = c.description,
            img = c.img,
            createdBy = c.createdBy,
            createdAt = c.createdAt,
            updatedBy = c.updatedBy,
            updatedAt = c.updatedAt,
            status = c.status,
            teacherModel = tm.first(),
            students = await get_student_by_course_id(db, c.id)
        )
        results.append(updated_course)

    return results

async def update_course(req, imgFile, db):
    data = dict(await req.form())
    old_data = db.query(CourseModel).filter(CourseModel.id == data['id']).first()

    if imgFile is not None:
        Path(os.getenv('COURSE_IMG_PATH')).mkdir(parents=True, exist_ok=True)

        # delete old img
        path = Path(os.getenv('COURSE_IMG_PATH')) / old_data.img
        if os.path.isfile(path):
            os.remove(path)

        # save old img
        fileName = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        path = Path(os.getenv('COURSE_IMG_PATH')) / fileName
        with path.open("wb") as buffer:
            shutil.copyfileobj(imgFile.file, buffer)
        old_data.img = fileName
        
    old_data.subject = data['subject']
    old_data.teacherId = data['teacherId']
    old_data.description = data['description']
    old_data.updatedBy = req.state.user.id
    old_data.updatedAt = func.current_timestamp()

    try:
        db.add(old_data)
        db.commit()

        old_student_courses = await get_student_course_by_course_id(db, data['id'])

        # delete all old student courses
        await delete_student_course_by_course_id(db, data['id'])

        # assign new updated students to new created course
        for s in json.loads(data['studentIds']):
            sc_data = StudentCourseModel(
                stuId = s,
                courseId = old_data.id,
                createdBy = req.state.user.id
            )

            # find old data
            filtered = [sc for sc in old_student_courses]
            if len(filtered) > 0:
                sc_data.joinDate = filtered[0].joinDate
                
            db.add(sc_data)
            db.commit()
        
        db.refresh(old_data)

    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to create course")
    
    return old_data

async def delete_course(req, db):
    id = dict(await req.form()).get('id')
    if id is None:
        raise HTTPException(status_code=400, detail="id is required")
    
    findData = db.query(CourseModel).filter(CourseModel.id == id).first()
    if not findData:
        raise HTTPException(status_code=422, detail="Not found")
    
    findData.status = 'D'

    try:
        db.add(findData)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to delete course")
    
    return JSONResponse(content="Deleted sucessfully")


async def get_only_courses_by_id(db, id):
    getData = db.query(CourseModel).filter(CourseModel.id == id).first()
    return getData



####### STUDENT COURSES #####

async def get_student_course_by_course_id(db, course_id):
    getData = db.query(StudentCourseModel).filter(StudentCourseModel.courseId == course_id).all()

    return getData

async def get_student_by_course_id(db, course_id):
    getData = db.query(StudentCourseModel).filter(StudentCourseModel.courseId == course_id).all()
    
    results = []
    for c in getData:
        student = await get_users({
            "id": c.stuId,
        }, db)

        if student is not None:
            results.append(student.first())

    return results

async def delete_student_course_by_course_id(db, course_id):
    getData = db.query(StudentCourseModel).filter(StudentCourseModel.courseId == course_id).all()
    
    try:
        for c in getData:
            db.delete(c)
        db.commit()
        return True
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to delete user")
    
async def get_course_by_student_id(db, stuId):
    getData = db.query(StudentCourseModel).filter(StudentCourseModel.stuId == stuId).all()
    return getData