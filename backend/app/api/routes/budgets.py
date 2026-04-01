from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import uuid
from app.core.db import db_client
from app.api.dependencies.auth import get_current_user

router = APIRouter(prefix="/budgets", tags=["budgets"])

# Simple model for budget
class BudgetCreate(BaseModel):
    category: str
    amount: float
    month: str
    notification_threshold: float = 80
    rollover_enabled: bool = False

class BudgetResponse(BaseModel):
    id: str
    user_id: str
    category: str
    amount: float
    month: str
    notification_threshold: float
    rollover_enabled: bool
    spent: float = 0
    remaining: float = 0
    created_at: str
    updated_at: str


@router.post("", response_model=BudgetResponse)
async def create_budget(
    budget: BudgetCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new budget"""
    budget_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    
    # Insert into database
    query = """
        INSERT INTO budgets (
            id, user_id, category, amount, month, 
            notification_threshold, rollover_enabled, 
            spent, remaining, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    db_client.execute_query(query, (
        budget_id,
        current_user["uid"],
        budget.category,
        budget.amount,
        budget.month,
        budget.notification_threshold,
        1 if budget.rollover_enabled else 0,
        0,  # spent
        budget.amount,  # remaining
        now,
        now
    ))
    
    # Return created budget
    return BudgetResponse(
        id=budget_id,
        user_id=current_user["uid"],
        category=budget.category,
        amount=budget.amount,
        month=budget.month,
        notification_threshold=budget.notification_threshold,
        rollover_enabled=budget.rollover_enabled,
        spent=0,
        remaining=budget.amount,
        created_at=now,
        updated_at=now
    )


@router.get("", response_model=List[BudgetResponse])
async def get_budgets(
    month: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Get all budgets for user"""
    if month:
        query = "SELECT * FROM budgets WHERE user_id = ? AND month = ?"
        results = db_client.fetch_all(query, (current_user["uid"], month))
    else:
        query = "SELECT * FROM budgets WHERE user_id = ?"
        results = db_client.fetch_all(query, (current_user["uid"],))
    
    budgets = []
    for row in results:
        budgets.append(BudgetResponse(
            id=row["id"],
            user_id=row["user_id"],
            category=row["category"],
            amount=row["amount"],
            month=row["month"],
            notification_threshold=row["notification_threshold"],
            rollover_enabled=bool(row["rollover_enabled"]),
            spent=row["spent"],
            remaining=row["remaining"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        ))
    
    return budgets


@router.get("/test")
async def test():
    """Test endpoint"""
    return {"message": "Budgets router is working!"}