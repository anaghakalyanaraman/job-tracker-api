from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserResponse
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

# 1. Health Check
@app.get("/health")
async def health():
    return {"status": "ok"}

# 2. Gets all users
@app.get("/users")
async def get_users(skip : int = 0 , limit : int = 10, db = Depends(get_db)):
    return db.query(User).offset(skip).limit(limit).all()

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
    db_user = User(name = user.name, email=user.email)
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

