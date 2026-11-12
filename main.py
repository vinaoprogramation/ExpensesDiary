from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, APIRouter, Depends

import time
import models
from database import Base, engine

from middlewares.request_time import log_requests
from middlewares.jwt_token import check_token

from routes.users import router as users_router
from routes.auth import router as auth_router
from routes.ai import router as ai_router
from routes.expenses import router as expenses_router

@asynccontextmanager
async def lifespan(app: FastAPI):
  Base.metadata.create_all(bind=engine)
  yield

app = FastAPI(
  title="Users API",
  version="1.0.0",
  lifespan=lifespan,
)


app.middleware("http")(log_requests)

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(ai_router)
app.include_router(expenses_router)
