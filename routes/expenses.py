from typing import Annotated

from fastapi import(
  APIRouter,
  Depends,
  HTTPException,
  Query,
  status
)

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, ProgrammingError, DataError, InterfaceError, InternalError
from sqlalchemy.orm import Session

from database import get_db
from models import Expenses
from schemas import UserCreate, UserUpdate, UserRead, ExpensesCreate
from security import hash_password
from middlewares.jwt_token import check_token

router = APIRouter(
  prefix="/expenses", 
  dependencies=[Depends(check_token)],
  tags=["Expenses"]
)

SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[dict, Depends(check_token)]

@router.get("/health", response_model=object, status_code=status.HTTP_200_OK)
def check_health():
  return {"mensagem": "olá"}


@router.post(
  "",
  response_model=ExpensesCreate,
  status_code=status.HTTP_201_CREATED
)
def create_expenses(payload: ExpensesCreate, db: SessionDep, token: TokenDep):

  id = token["sub"]

  expenses = Expenses(
    expenses=payload.expenses,
    user_id=id
  )

  db.add(expenses)  

  try:
    db.commit()
  except (IntegrityError, OperationalError, ProgrammingError, DataError, InterfaceError, InternalError):
    db.rollback()
    raise HTTPException(
      status_code=500,
      detail="Erro interno no banco de dados"  
    )
  db.refresh(expenses)

  return expenses

