from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import jwt
from core.security import get_current_user
from users.routes import router as user_router
from auth.route import router as auth_router
from courses.routes import router as course_router
from schedule.routes import router as schedule_router
from attendances.routes import router as att_router
from dashboard.routes import router as dashboard_router

app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(course_router)
app.include_router(schedule_router)
app.include_router(att_router)
app.include_router(dashboard_router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Add Middleware
@app.middleware("http")
async def jwt_middleware(request: Request, call_next):
    print(request.url.path)
    allowed_paths = [
        "/",
        "/api/v1/auth/login",
        "/api/v1/auth/register",
        "/docs",
        "/redoc",
        "/openapi.json"
    ]
    if request.url.path in allowed_paths or request.url.path.startswith("/uploads/"):
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"detail": "Missing token"})

    token = auth_header.split(" ")[1]

    try:
        request.state.user = get_current_user(token)
        if request.state.user is None:
            return JSONResponse(status_code=401, content={"detail": "Invalid credentials"})
    except jwt.ExpiredSignatureError:
        return JSONResponse(status_code=401, content={"detail": "Token expired"})
    except jwt.InvalidTokenError:
        return JSONResponse(status_code=401, content={"detail": "Invalid token"})

    return await call_next(request)

@app.get('/')
def index():
    return JSONResponse(content={"status": "Welcome to Student Attendance API"})