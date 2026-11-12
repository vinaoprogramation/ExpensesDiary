from pydantic import BaseModel, ConfigDict, EmailStr, Field, Json
import json
from typing import Any, Literal

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
  reports: str

class ChatRequest(BaseModel):
  prompt: str
  


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

class FinancialSummary(StrictModel):
    net_salary: float
    total_expenses: float
    expenses_percentage: float
    remaining_balance: float
    remaining_percentage: float


class ExpenseItem(StrictModel):
    category: str
    amount: float
    salary_percentage: float
    type: str
    group: Literal["necessities", "wants", "savings", "impulse"]


class Goal(StrictModel):
    description: str
    target_amount: float
    target_months: int
    required_monthly_savings: float
    required_salary_percentage: float
    is_viable_currently: bool


class ImbalanceCriterion(StrictModel):
    name: str
    description: str
    ideal_range_percentage: list[float]
    current_percentage: float
    current_amount: float
    status: Literal[
        "within_range",
        "attention_needed",
        "ok_but_insufficient_for_goal",
        "optimizable",
        "critical",
    ]
    deviation_note: str


class ImbalanceAnalysis(StrictModel):
    criteria: list[ImbalanceCriterion]
    conclusions: list[str]


class ExpenseCutItem(StrictModel):
    category: str
    proposal: str
    monthly_savings: float


class ExpenseCuts(StrictModel):
    items: list[ExpenseCutItem]
    total_potential_savings: float


class ReallocationSource(StrictModel):
    source: str
    amount: float


class ResourceReallocation(StrictModel):
    sources: list[ReallocationSource]
    new_monthly_available_for_goal: float


class RemainingGap(StrictModel):
    monthly_deficit: float
    alternatives: list[str]


class MonthProjection(StrictModel):
    month: int
    initial_balance: float
    cut_savings: float
    redirected_investments: float
    total_for_goal: float
    comment: str


class MonthlyProjection(StrictModel):
    months: list[MonthProjection]
    accumulated_3_months: float
    missing_after_3_months: float
    alternative_timeline_months: int
    accumulated_4_months: float


class Strategy(StrictModel):
    expense_cuts: ExpenseCuts
    resource_reallocation: ResourceReallocation
    remaining_gap: RemainingGap
    monthly_projection: MonthlyProjection


class PracticalRecommendation(StrictModel):
    area: str
    action: str
    expected_impact: str


class ScheduleItem(StrictModel):
    period: str
    tasks: list[str]


class SummaryHighlight(StrictModel):
    topic: str
    detail: str


class QuickSummary(StrictModel):
    highlights: list[SummaryHighlight]
    closing_message: str


class FinancialReport(StrictModel):
    user_id: str
    report_title: str
    currency: str
    financial_summary: FinancialSummary
    expenses_breakdown: list[ExpenseItem]
    goal: Goal
    imbalance_analysis: ImbalanceAnalysis
    strategy: Strategy
    practical_recommendations: list[PracticalRecommendation]
    schedule: list[ScheduleItem]
    quick_summary: QuickSummary