from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, students
from db.session import Base, engine
from db.seed import seed_if_needed
from core.config import settings

app = FastAPI(
    title="Student Management API",
    description="Simple teaching API with signup, login (JWT), and student CRUD.",
    version="0.2.0",
)

# CORS
origins = settings.allowed_origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables & seed on startup (idempotent)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    seed_if_needed()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(students.router, prefix="/students", tags=["students"])

@app.get("/")
def root():
    return {"message": "Student Management API is running."}
