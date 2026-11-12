from typing import Annotated
import os
from fastapi import(
  APIRouter,
  Depends,
  HTTPException,
  Query,
  status
)
import httpx
import traceback

from dotenv import load_dotenv
from groq import AsyncGroq
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, ProgrammingError, DataError, InterfaceError, InternalError
from sqlalchemy.orm import Session

from database import get_db
from models import Expenses
from schemas import UserCreate, UserUpdate, UserRead, ExpensesCreate, ReportsRead
from security import hash_password
from middlewares.jwt_token import check_token

router = APIRouter(
  prefix="/reports", 
  dependencies=[Depends(check_token)],
  tags=["Reports"]
)

SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[dict, Depends(check_token)]

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("A varável da API não existe")

http_client = httpx.AsyncClient(verify=False)

groq_client = AsyncGroq(
  api_key=os.getenv("GROQ_API_KEY"),
  http_client=http_client
)

@router.get("/health", response_model=object, status_code=status.HTTP_200_OK)
def check_health():
  return {"mensagem": "olá"}


@router.post(
  "/{expenses_id}",
  response_model=ReportsRead,
  status_code=status.HTTP_200_OK
)
async def generate_reports(db: SessionDep, expenses_id: int, token: TokenDep):
  id = {expenses_id}

  user_id = token["sub"]

  if not id:
    raise HTTPException(
      status_code=403,
      detail="Bad request"
    )
  
  if not user_id:
    raise HTTPException(
      status_code=403,
      detail="Bad request"
    )
  
  query = select(Expenses)
  
  query = query.where(Expenses.id == id)
  query = query.where(Expenses.user_id == user_id)

  expenses = db.scalars(query).all()

  print(expenses)

  if expenses is None:
    raise HTTPException(
       status_code=404,
       detail="Expenses not found"
    )

  try:
      completion = await groq_client.chat.completions.create(
          model="openai/gpt-oss-120b",
          messages=[{"role": "user", "content": "Gere um relatório sobre os seguintes gastos, destacando formas de poupar dinheiro e como organiza-los: {expenses}"}],
          temperature=0.7
      )

      return str({"response": completion.choices[0].message.content})

  except Exception as e:
      traceback.print_exc()
      raise HTTPException(status_code=500, detail=str(e))

