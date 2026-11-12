from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from schemas import LoginInput
from database import get_db
from models import User
from security import (
  verify_password,
  create_acess_token,
)

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(
  payload: LoginInput,
  db: Annotated[Session, Depends(get_db)]
):
  user = db.scalar(
    select(User).where(
      User.email == payload.email.lower()
    )
  )

  if not user or not verify_password(
    payload.password,
    user.password_hash,
  ):
    raise HTTPException(
      status_code=401,
      detail="Credenciais inválidas",
      headers={"WWW-Authenticate": "Bearer"}
    )

  token = create_acess_token(user.id)

  return {
    "acess_token": token,
    "token_type": "bearer"
  }

