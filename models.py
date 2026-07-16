from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey
from typing import Optional

class User(Base):
    __tablename__ = "users"
    id : Mapped[int] = mapped_column(primary_key = True)
    name : Mapped[str] = mapped_column(String(100))
    email : Mapped[str] = mapped_column(String(100), unique = True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    hashed_password: Mapped[str] = mapped_column(String(255))
    
class Job(Base):
    __tablename__ = "jobs"
    id : Mapped[int] = mapped_column(primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    company : Mapped[str] = mapped_column(String(100))
    role : Mapped[str] = mapped_column(String(100))
    status : Mapped[str] = mapped_column(String(50), default = "Applied")
    notes : Mapped[Optional[str]] = mapped_column(String(500), nullable = True)
    applied_date : Mapped[datetime] = mapped_column(DateTime, default= datetime.utcnow)