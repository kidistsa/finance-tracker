from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.recurring_transaction import (
    RecurringTransaction, RecurringTransactionCreate, 
    RecurringTransactionUpdate
)
from app.repositories.recurring_repo import RecurringRepository
from app.api.dependencies.auth import get_current_user

router = APIRouter(prefix="/recurring", tags=["Recurring Transactions"])


async def get_recurring_repo():
    return RecurringRepository()


@router.post("", response_model=RecurringTransaction)
async def create_recurring(
    recurring: RecurringTransactionCreate,
    current_user: dict = Depends(get_current_user),
    repo: RecurringRepository = Depends(get_recurring_repo)
):
    """Create a new recurring transaction"""
    recurring.user_id = current_user["uid"]
    recurring_id = await repo.create(recurring)
    
    created = await repo.get(recurring_id)
    return RecurringTransaction(**created)


@router.get("", response_model=List[RecurringTransaction])
async def get_user_recurring(
    current_user: dict = Depends(get_current_user),
    repo: RecurringRepository = Depends(get_recurring_repo)
):
    """Get all recurring transactions for the current user"""
    recurring = await repo.get_user_recurring(current_user["uid"])
    return [RecurringTransaction(**r) for r in recurring]


@router.put("/{recurring_id}", response_model=RecurringTransaction)
async def update_recurring(
    recurring_id: str,
    update_data: RecurringTransactionUpdate,
    current_user: dict = Depends(get_current_user),
    repo: RecurringRepository = Depends(get_recurring_repo)
):
    """Update a recurring transaction"""
    existing = await repo.get(recurring_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Recurring transaction not found")
    
    if existing.get("user_id") != current_user["uid"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    await repo.update_recurring(recurring_id, update_data)
    
    updated = await repo.get(recurring_id)
    return RecurringTransaction(**updated)


@router.delete("/{recurring_id}")
async def delete_recurring(
    recurring_id: str,
    current_user: dict = Depends(get_current_user),
    repo: RecurringRepository = Depends(get_recurring_repo)
):
    """Delete a recurring transaction"""
    existing = await repo.get(recurring_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Recurring transaction not found")
    
    if existing.get("user_id") != current_user["uid"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    await repo.delete_recurring(recurring_id)
    return {"message": "Recurring transaction deleted"}


@router.post("/process")
async def process_recurring(
    repo: RecurringRepository = Depends(get_recurring_repo)
):
    """Process all due recurring transactions (run by scheduler)"""
    created = await repo.process_due_transactions()
    return {"created": len(created)}