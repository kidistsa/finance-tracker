from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from .transaction import TransactionCategory


class BudgetBase(BaseModel):
    """Base budget model"""
    category: TransactionCategory
    amount: float = Field(..., gt=0)
    month: str = Field(..., pattern=r"^\d{4}-\d{2}$")  # Format: YYYY-MM
    notification_threshold: float = 80  # Percentage at which to send alert
    rollover_enabled: bool = False


class BudgetCreate(BudgetBase):
    """Model for creating a budget"""
    user_id: str  # This will be set from the authenticated user


class BudgetUpdate(BaseModel):
    """Model for updating a budget"""
    amount: Optional[float] = Field(None, gt=0)
    notification_threshold: Optional[float] = Field(None, ge=0, le=100)
    rollover_enabled: Optional[bool] = None


class Budget(BudgetBase):
    """Complete budget model"""
    id: str
    user_id: str
    spent: float = 0
    remaining: float = 0
    percentage_used: float = 0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class BudgetAlert(BaseModel):
    """Budget alert model"""
    budget_id: str
    category: TransactionCategory
    threshold: float
    current_percentage: float
    message: str
    created_at: datetime