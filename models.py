from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from datetime import datetime
from sqlalchemy import DateTime

class User(Base):
    __tablename__ = "users"
    id : Mapped[int] = mapped_column(primary_key = True)
    name : Mapped[str] = mapped_column(String(100))
    email : Mapped[str] = mapped_column(String(100), unique = True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)