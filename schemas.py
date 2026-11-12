from pydantic import BaseModel, ConfigDict, EmailStr, Field, Json
import json
from typing import Any

class UserCreate(BaseModel):
  model_config = ConfigDict(str_strip_whitespace=True)

  name: str = Field(min_length=2, max_length=120)
  email: EmailStr
  password: str = Field(min_length=6, max_length=120)

class UserUpdate(BaseModel):
  model_config = ConfigDict(str_strip_whitespace=True)

  name: str | None = Field(
    default=None,
    min_length=2,
    max_length=120
  )
  email: EmailStr | None = None
  password: str | None = Field(min_length=6, max_length=120)

class UserRead(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id: int
  name: str
  email: EmailStr

class LoginInput(BaseModel):
  email: EmailStr
  password: str

class ExpensesCreate(BaseModel):
  expenses: dict[str, Any] = Field(max_length=1000)

class ReportsRead(BaseModel):
  reports: str = Field(max_length=3000)

class ChatRequest(BaseModel):
  prompt: str
  