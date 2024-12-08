from datetime import datetime, timedelta
from attendances.models import AttendanceModel
from courses.services import get_course_by_student_id, get_only_courses_by_id
from dashboard.schemas import DashboardResponseModel
from schedule.models import ScheduleModel

async def get_dashbaord_data(req, db):
    now = datetime.now()
    result = DashboardResponseModel()

    if(req.state.user.type == 1): # student
        # get current course
        stu_courses = await get_course_by_student_id(db, req.state.user.id)
        course_ids = [sc.courseId for sc in stu_courses]

        schedule = db.query(ScheduleModel).filter(
            ScheduleModel.courseId.in_(course_ids),
            ScheduleModel.startTime <= now,
            ScheduleModel.endTime >= now
        ).first()
        if schedule is not None:
            result.course = await get_only_courses_by_id(db, schedule.courseId)

            # get current course attendance
            result.attendances = db.query(AttendanceModel).filter(
                AttendanceModel.courseId == result.course.id,
                AttendanceModel.stuId == req.state.user.id,
                AttendanceModel.createdAt >= schedule.startTime,
            ).all()
    
    return result