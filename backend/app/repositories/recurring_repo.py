from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from .base import BaseRepository
from app.models.recurring_transaction import RecurringTransactionCreate, RecurringTransactionUpdate,RecurringFrequency
import uuid


class RecurringRepository(BaseRepository):
    """Repository for recurring transactions"""
    
    def __init__(self):
        super().__init__("recurring_transactions")
    
    async def create(self, recurring: RecurringTransactionCreate) -> str:
        """Create a new recurring transaction"""
        recurring_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        # Calculate next occurrence
        next_occurrence = self._calculate_next_occurrence(
            recurring.start_date, 
            recurring.frequency
        )
        
        data = {
            "id": recurring_id,
            "user_id": recurring.user_id,
            "name": recurring.name,
            "amount": recurring.amount,
            "category": recurring.category,
            "transaction_type": recurring.transaction_type,
            "frequency": recurring.frequency.value,
            "start_date": recurring.start_date.isoformat(),
            "end_date": recurring.end_date.isoformat() if recurring.end_date else None,
            "active": 1 if recurring.active else 0,
            "next_occurrence": next_occurrence.isoformat(),
            "last_occurrence": None,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat()
        }
        
        self.create(data)
        return recurring_id
    
    async def get_user_recurring(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all recurring transactions for a user"""
        return self.list({"user_id": user_id})
    
    async def update_recurring(self, recurring_id: str, update_data: RecurringTransactionUpdate) -> bool:
        """Update a recurring transaction"""
        update_dict = {}
        if update_data.name is not None:
            update_dict["name"] = update_data.name
        if update_data.amount is not None:
            update_dict["amount"] = update_data.amount
        if update_data.category is not None:
            update_dict["category"] = update_data.category
        if update_data.frequency is not None:
            update_dict["frequency"] = update_data.frequency.value
            # Recalculate next occurrence
            existing = self.get(recurring_id)
            if existing:
                start_date = datetime.fromisoformat(existing["start_date"])
                update_dict["next_occurrence"] = self._calculate_next_occurrence(start_date, update_data.frequency).isoformat()
        if update_data.end_date is not None:
            update_dict["end_date"] = update_data.end_date.isoformat()
        if update_data.active is not None:
            update_dict["active"] = 1 if update_data.active else 0
        
        if update_dict:
            update_dict["updated_at"] = datetime.utcnow().isoformat()
            return self.update(recurring_id, update_dict)
        return True
    
    async def delete_recurring(self, recurring_id: str) -> bool:
        """Delete a recurring transaction"""
        return self.delete(recurring_id)
    
    async def get_due_transactions(self) -> List[Dict[str, Any]]:
        """Get all recurring transactions that are due today"""
        today = datetime.utcnow().date()
        all_recurring = self.list({})
        due = []
        
        for r in all_recurring:
            if not r.get("active"):
                continue
            
            next_date = datetime.fromisoformat(r["next_occurrence"]).date()
            if next_date <= today:
                due.append(r)
        
        return due
    
    async def process_due_transactions(self):
        """Process all due recurring transactions and create actual transactions"""
        due = await self.get_due_transactions()
        created_transactions = []
        
        for recurring in due:
            # Create actual transaction
            from app.models.transaction import TransactionCreate
            from app.repositories.transaction_repo import TransactionRepository
            
            transaction_data = TransactionCreate(
                user_id=recurring["user_id"],
                amount=recurring["amount"],
                description=recurring["name"],
                category=recurring["category"],
                transaction_type=recurring["transaction_type"],
                date=datetime.utcnow(),
                source="recurring"
            )
            
            tx_repo = TransactionRepository()
            created = await tx_repo.create_transaction(transaction_data)
            created_transactions.append(created)
            
            # Update next occurrence
            frequency = RecurringFrequency(recurring["frequency"])
            current_next = datetime.fromisoformat(recurring["next_occurrence"])
            new_next = self._calculate_next_occurrence(current_next, frequency)
            
            self.update(recurring["id"], {
                "next_occurrence": new_next.isoformat(),
                "last_occurrence": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            })
        
        return created_transactions
    
    def _calculate_next_occurrence(self, start_date: datetime, frequency: RecurringFrequency) -> datetime:
        """Calculate the next occurrence date"""
        now = datetime.utcnow()
        next_date = start_date
        
        while next_date <= now:
            if frequency == RecurringFrequency.DAILY:
                next_date += timedelta(days=1)
            elif frequency == RecurringFrequency.WEEKLY:
                next_date += timedelta(weeks=1)
            elif frequency == RecurringFrequency.MONTHLY:
                # Add month (handle year rollover)
                if next_date.month == 12:
                    next_date = next_date.replace(year=next_date.year + 1, month=1)
                else:
                    next_date = next_date.replace(month=next_date.month + 1)
            elif frequency == RecurringFrequency.YEARLY:
                next_date = next_date.replace(year=next_date.year + 1)
        
        return next_date