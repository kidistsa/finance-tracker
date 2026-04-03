from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class RecurringFrequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class RecurringTransactionBase(BaseModel):
    name: str = Field(..., max_length=100)
    amount: float = Field(..., gt=0)
    category: str
    transaction_type: str  # "expense" or "income"
    frequency: RecurringFrequency
    start_date: datetime
    end_date: Optional[datetime] = None
    active: bool = True


class RecurringTransactionCreate(RecurringTransactionBase):
    user_id: str


class RecurringTransactionUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[str] = None
    frequency: Optional[RecurringFrequency] = None
    end_date: Optional[datetime] = None
    active: Optional[bool] = None


class RecurringTransaction(RecurringTransactionBase):
    id: str
    user_id: str
    next_occurrence: datetime
    last_occurrence: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime