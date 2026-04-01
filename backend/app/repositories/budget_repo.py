from typing import List, Dict, Any, Optional
from datetime import datetime
from .base import BaseRepository
from app.models.budget import BudgetCreate, BudgetUpdate
import uuid


class BudgetRepository(BaseRepository):
    """Budget repository"""
    
    def __init__(self):
        super().__init__("budgets")
    
    async def create_budget(self, budget: BudgetCreate) -> str:
        """Create a new budget"""
        budget_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        budget_data = {
            "id": budget_id,
            "user_id": budget.user_id,
            "category": budget.category.value,
            "amount": budget.amount,
            "month": budget.month,
            "notification_threshold": budget.notification_threshold,
            "rollover_enabled": 1 if budget.rollover_enabled else 0,
            "spent": 0,
            "remaining": budget.amount,
            "percentage_used": 0,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat()
        }
        
        # Save using base class create method
        self.create(budget_data)
        return budget_id
    
    async def get_budget(self, budget_id: str) -> Optional[Dict[str, Any]]:
        """Get budget by ID"""
        return self.get(budget_id)
    
    async def update_budget(self, budget_id: str, budget: BudgetUpdate) -> bool:
        """Update budget"""
        update_data = {}
        if budget.amount is not None:
            update_data["amount"] = budget.amount
            update_data["remaining"] = budget.amount - update_data.get("spent", 0)
        if budget.notification_threshold is not None:
            update_data["notification_threshold"] = budget.notification_threshold
        if budget.rollover_enabled is not None:
            update_data["rollover_enabled"] = 1 if budget.rollover_enabled else 0
        
        if update_data:
            update_data["updated_at"] = datetime.utcnow().isoformat()
            return self.update(budget_id, update_data)
        return True
    
    async def delete_budget(self, budget_id: str) -> bool:
        """Delete budget"""
        return self.delete(budget_id)
    
    async def get_user_budgets(
        self, 
        user_id: str, 
        month: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get user budgets"""
        filters = {"user_id": user_id}
        if month:
            filters["month"] = month
        
        return self.list(filters)
    
    async def get_budget_by_category(
        self, 
        user_id: str, 
        category: str, 
        month: str
    ) -> Optional[Dict[str, Any]]:
        """Get budget by category and month"""
        filters = {
            "user_id": user_id,
            "category": category,
            "month": month
        }
        budgets = self.list(filters, limit=1)
        return budgets[0] if budgets else None