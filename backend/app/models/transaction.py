from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"


class TransactionCategory(str, Enum):
    # Income
    SALARY = "salary"
    FREELANCE = "freelance"
    INVESTMENT = "investment"
    GIFT = "gift"
    OTHER_INCOME = "other_income"
    
    # Expenses
    HOUSING = "housing"
    TRANSPORTATION = "transportation"
    FOOD_GROCERIES = "food_groceries"
    FOOD_DINING = "food_dining"
    UTILITIES = "utilities"
    INSURANCE = "insurance"
    HEALTHCARE = "healthcare"
    SAVINGS = "savings"
    PERSONAL = "personal"
    ENTERTAINMENT = "entertainment"
    EDUCATION = "education"
    DEBT = "debt"
    SHOPPING = "shopping"
    TRAVEL = "travel"
    OTHER_EXPENSE = "other_expense"


class TransactionSource(str, Enum):
    CSV_UPLOAD = "csv_upload"
    PLAID_SYNC = "plaid_sync"
    MANUAL = "manual"
    API = "api"


class TransactionBase(BaseModel):
    """Base transaction model"""
    amount: float = Field(..., gt=0, description="Transaction amount (positive number)")
    description: str = Field(..., min_length=1, max_length=500)
    category: TransactionCategory = TransactionCategory.OTHER_EXPENSE
    transaction_type: TransactionType
    date: datetime
    source: TransactionSource = TransactionSource.MANUAL  # ✅ Add this field
    account_id: Optional[str] = None
    merchant_name: Optional[str] = None
    notes: Optional[str] = None
    tags: List[str] = []
    is_recurring: bool = False
    
    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v


class TransactionCreate(TransactionBase):
    """Model for creating a transaction"""
    user_id: str


class TransactionUpdate(BaseModel):
    """Model for updating a transaction"""
    category: Optional[TransactionCategory] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    is_recurring: Optional[bool] = None


class Transaction(TransactionBase):
    """Complete transaction model"""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TransactionSummary(BaseModel):
    """Transaction summary for dashboard"""
    total_income: float
    total_expenses: float
    net_savings: float
    transaction_count: int
    period_start: datetime
    period_end: datetime


class TransactionFilters(BaseModel):
    """Transaction filters"""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    categories: Optional[List[TransactionCategory]] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    search: Optional[str] = None