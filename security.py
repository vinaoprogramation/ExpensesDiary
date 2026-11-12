import os
import jwt

from datetime import datetime, timedelta, timezone

JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGORITHM = "HS256"

from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
  return password_hash.hash(password)

def verify_password(
  password: str,
  stored_hash: str,
) -> bool:
  return password_hash.verify(
    password,
    stored_hash
  )

def create_acess_token(user_id: int) -> str:
  expiration = (
    datetime.now(timezone.utc)
    + timedelta(minutes=30)
  )

  return jwt.encode(
    {
      "sub": str(user_id),
      "exp": expiration,
    },
    JWT_SECRET,
    algorithm=JWT_ALGORITHM,
  )

