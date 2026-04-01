from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class RecurringFrequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class RecurringTransactionBase(BaseModel):
    name: str
    amount: float = Field(..., gt=0)
    category: str
    transaction_type: str
    frequency: RecurringFrequency
    start_date: datetime
    end_date: Optional[datetime] = None
    next_occurrence: datetime
    active: bool = True

class RecurringTransactionCreate(RecurringTransactionBase):
    user_id: str

class RecurringTransaction(RecurringTransactionBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime