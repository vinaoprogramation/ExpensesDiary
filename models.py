from enum import Enum as PyEnum
from sqlalchemy import Integer, String, Enum, JSON, DateTime, Boolean, true
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from database import Base

#class Is_Active(PyEnum):
  #ON = "on"
  #OFF = "off"

class User(Base):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(
    Integer,
    primary_key=True,
    autoincrement=True
  )

  name: Mapped[str] = mapped_column(
    String(120),
    nullable=False,
  )

  email: Mapped[str] = mapped_column(
    String(320),
    unique=True,
    index=True,
    nullable=False,
  )

  password_hash: Mapped[str] = mapped_column(
    String(255),
    nullable=False
  )

class Expenses(Base):
  __tablename__ = "expenses"

  id: Mapped[int] = mapped_column(
    Integer,
    primary_key=True,
    autoincrement=True
  )

  expenses: Mapped[JSON] = mapped_column(
    JSON,
    nullable=False,
  )

  on_date: Mapped[DateTime] = mapped_column(
    DateTime(timezone=True), 
    server_default=func.now(),
    nullable=False,
  )

  is_active: Mapped[bool] = mapped_column(
    Boolean,
    server_default=true(),
    nullable=False,
  )

class Reports(Base):
  __tablename__ = "reports"
  
  id: Mapped[int] = mapped_column(
    Integer,
    primary_key=True,
    autoincrement=True    
  )
  
  report: Mapped[JSON] = mapped_column(
    JSON,
    nullable=False,
  )
  
  on_date: Mapped[DateTime] = mapped_column(
    DateTime(timezone=True), 
    server_default=func.now(),
    nullable=False,
  )
  
  is_active: Mapped[bool] = mapped_column(
    Boolean,
    server_default=true(),
    nullable=False,
  )