from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email : str
    password : str
    @field_validator('name')
    @classmethod
    def name_validator(cls, value):
            if len(value.strip())<2:
                  raise ValueError("Name must be atleast 2 charecters")
            return value
    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
          if '.' not in value or '@' not in value:
                raise ValueError("Enter a proper email")
          return value
    @field_validator('password')
    @classmethod
    def password_validator(cls, value):
          if len(value.strip())<6:
                raise ValueError("Password must be atleast 6 charecters")
          return value
          
    
class UserResponse(BaseModel):
      id : int
      name: str
      email : str
      created_at: datetime

class Token (BaseModel):
      access_token : str
      token_type : str

class UserLogin (BaseModel):
      email : str
      password : str

class JobCreate(BaseModel):
      company : str
      role : str
      status : str = "Applied"
      notes : Optional[str]

class JobResponse(BaseModel):
      id : int
      user_id : int
      company : str
      role :str
      status : str
      notes : Optional[str]
      applied_date : datetime