from typing import Annotated

from fastapi import(
  APIRouter,
  Depends,
  HTTPException,
  Query,
  status
)

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import UserCreate, UserUpdate, UserRead
from security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])

SessionDep = Annotated[Session, Depends(get_db)]

def get_user_or_404(user_id: int, db: Session) -> User:
  user = db.get(User, user_id)

  if user is None:
    raise HTTPException(
      status_code=404,
      detail="Usuário não encontrado"
    )

  return user

@router.get("/health", response_model=object, status_code=status.HTTP_200_OK)
def check_health():
  return {"mensagem": "olá"}

@router.post(
  "",
  response_model=UserRead,
  status_code=status.HTTP_201_CREATED,
)
def create_user(payload: UserCreate, db: SessionDep):
  user = User(
    name=payload.name,
    email=str(payload.email).lower(),
    password_hash=hash_password(payload.password)
  )

  db.add(user)

  try:
    db.commit()
  except IntegrityError:
    db.rollback()
    raise HTTPException(
      status_code=409,
      detail="E-mail já cadastrado"
    )

  db.refresh(user)


  return user

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: SessionDep):
  return get_user_or_404(user_id, db)

@router.patch("/{user_id}", response_model=UserRead)
def update_user(
  user_id: int,
  payload: UserUpdate,
  db: SessionDep,
):
  user = get_user_or_404(user_id, db)

  changes = payload.model_dump(exclude_unset=True)

  if any(value is None for value in changes.value()):
    raise HTTPException(
      status_code=422,
      detail="Os campos não pode ser nulos",
    )

  if "email" in changes:
    changes["email"] = changes["email"].lower()

  for field, value in changes.items():
    setattr(user, field, value)

  try:
    db.commit()
  except IntegrityError:
    db.rollback()
    raise HTTPException(
      status_code=409,
      detail="E-mail já cadastrado",
    )

  db.refresh(user)

  return user

@router.delete(
  "/{user_id}",
  status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(user_id: int, db: SessionDep):
  user = get_user_or_404(user_id, db)

  db.delete(user)
  db.commit()


