import time
from fastapi import APIRouter, Request, FastAPI

import jwt
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
from models import User
from security import JWT_SECRET, JWT_ALGORITHM

async def check_token(request: Request):

  auth_header = request.headers.get("authorization")

  credentials_exception = HTTPException(
    status_code=401,
    detail="Authorization not valid",
    headers={"WWW-Authenticate": "Bearer"},
  )

  if not auth_header or not auth_header.startswith("Bearer "):
    raise credentials_exception

  try:

    token = auth_header.split(" ")[1]

    payload = jwt.decode(
      token,
      JWT_SECRET,
      algorithms=[JWT_ALGORITHM],
      options={"require": ["sub", "exp"]}
    )

    return payload

  except (jwt.InvalidTokenError, ValueError, TypeError):
    raise credentials_exception
  
  


  