from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from users.routes import router as guest_router
from auth.route import router as auth_router
from core.security import JWTAuth
from starlette.middleware.authentication import AuthenticationMiddleware


app = FastAPI()
app.include_router(guest_router)
app.include_router(auth_router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Add Middleware
# app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())

@app.get('/')
def health_check():
    return JSONResponse(content={"status": "Welcome to Student Attendance API"})