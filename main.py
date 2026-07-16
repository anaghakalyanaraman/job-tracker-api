from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User, Job
from schemas import UserCreate, UserResponse
from schemas import JobCreate, JobResponse
from database import Base, engine
from auth import hash_password, verify_password, create_access_token, get_current_user
from schemas import Token, UserLogin
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 1. Health Check
@app.get("/health")
async def health():
    return {"status": "ok"}

# 2. Gets all users
@app.get("/users")
async def get_users(skip : int = 0 , limit : int = 10, db = Depends(get_db)):
    return db.query(User).offset(skip).limit(limit).all()

# Get Present user
@app.get("/users/me")
async def present_user(current_user = Depends(get_current_user)):
    return current_user

#3. Get one user
@app.get("/users/{user_id}")
async def get_user(user_id: int, db = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return db_user

#4. Create User
@app.post("/users", response_model = UserResponse)
async def create_user(user : UserCreate, db = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=409, detail="Email already exists")
    hpass = hash_password(user.password)
    db_user = User(name = user.name, email=user.email, hashed_password = hpass)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#5. Update User
@app.put("/users/{user_id}", response_model= UserResponse)
async def update_user(user_id : int, user: UserCreate, db = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.name =  user.name
        db_user.email = user.email
        db.commit()
        db.refresh(db_user)   
        return db_user
    raise HTTPException(status_code = 404, detail = "User Not Found")

#6. Delete User
@app.delete("/users/{user_id}", response_model= UserResponse)
async def delete_user(user_id: int, db = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    else:
        raise HTTPException(status_code = 404 , detail = "User Not Found")

#7. Post /auth/register
@app.post("/auth/register", response_model= UserResponse)
async def register_user(user : UserCreate, db = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=409, detail="Email already exists")
    hpass = hash_password(user.password)
    db_user = User(name = user.name, email = user.email, hashed_password = hpass)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#8. post /auth/login
@app.post("/auth/login", response_model= Token)
async def login_auth(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    db_user = db.query(User).filter(User.email == form_data.username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Email not found")
    if not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Wrong password")
    token = create_access_token({"sub": db_user.email}, timedelta(minutes=30))
    return Token(access_token=token, token_type="bearer")

@app.get("/jobs")
async def get_jobs(current_user = Depends(get_current_user), db = Depends(get_db)):
    jobs = db.query(Job).filter(Job.user_id == current_user.id).all()
    return jobs

@app.post("/jobs", response_model = JobResponse)
async def create_jobs( job : JobCreate, current_user = Depends(get_current_user), db = Depends(get_db)):
    db_job = Job(user_id = current_user.id, company = job.company, role = job.role, status = job.status, notes = job.notes)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@app.delete("/jobs/{jobs_id}", response_model= JobResponse)
async def delete_job(jobs_id : int, current_user = Depends(get_current_user), db = Depends(get_db)):
    db_job = db.query(Job).filter(Job.id == jobs_id, Job.user_id == current_user.id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(db_job)
    db.commit()
    return db_job

@app.put("/jobs/{job_id}", response_model = JobResponse)
async def update_job(job : JobCreate, job_id : int, current_user = Depends(get_current_user), db = Depends(get_db)):
    db_job = db.query(Job).filter(Job.id == job_id, Job.user_id == current_user.id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    db_job.company = job.company
    db_job.role = job.role
    db_job.status = job.status
    db_job.notes = job.notes
    db.commit()
    db.refresh(db_job)
    return db_job

