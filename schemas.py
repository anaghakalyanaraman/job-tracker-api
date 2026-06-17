from pydantic import BaseModel, field_validator
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email : str
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
    
class UserResponse(BaseModel):
      id : int
      name: str
      email : str
      created_at: datetime