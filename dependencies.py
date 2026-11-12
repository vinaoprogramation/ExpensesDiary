from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .database import get_db
from .models import User
from .security import JWT_SECRET, JWT_ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(
  tokenUrl="/auth/login"
)

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)]
):
  error = HTTPException(
    status_code=401,
    detail="Token inválido ou expirado",
    headers={"WWW-Authenticate": "Bearer"}
  )

  try:
    payload = jwt.decode(
      token,
      JWT_SECRET,
      algorithms=[JWT_ALGORITHM],
      options={"require": ["sub", "exp"]}
    )
    user_id = int(payload["sub"])

  except (jwt.InvalidTokenError, ValueError, TypeError):
    raise error

  user = db.get(User, user_id)

  if user is None:
    raise error

  return user