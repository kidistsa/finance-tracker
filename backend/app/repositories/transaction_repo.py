from typing import List, Dict, Any, Optional
from datetime import datetime
from .base import BaseRepository
from app.models.transaction import TransactionCreate, TransactionUpdate, Transaction
from app.core.db import db_client
import uuid


class TransactionRepository(BaseRepository):
    
    def __init__(self):
        super().__init__("transactions")
    
    async def create_transaction(self, transaction: TransactionCreate) -> Transaction:
        transaction_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        transaction_data = {
            "id": transaction_id,
            "user_id": transaction.user_id,
            "amount": transaction.amount,
            "description": transaction.description,
            "category": transaction.category.value if hasattr(transaction.category, 'value') else transaction.category,
            "transaction_type": transaction.transaction_type.value if hasattr(transaction.transaction_type, 'value') else transaction.transaction_type,
            "date": transaction.date.isoformat(),
            "source": transaction.source.value if hasattr(transaction.source, 'value') else transaction.source,
            "account_id": transaction.account_id,
            "merchant_name": transaction.merchant_name,
            "notes": transaction.notes,
            "tags": ",".join(transaction.tags) if transaction.tags else "",
            "is_recurring": 1 if transaction.is_recurring else 0,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat()
        }
        
        query = """
            INSERT INTO transactions (
                id, user_id, amount, description, category, 
                transaction_type, date, source, account_id, 
                merchant_name, notes, tags, is_recurring, 
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        db_client.execute_query(query, (
            transaction_data["id"],
            transaction_data["user_id"],
            transaction_data["amount"],
            transaction_data["description"],
            transaction_data["category"],
            transaction_data["transaction_type"],
            transaction_data["date"],
            transaction_data["source"],
            transaction_data["account_id"],
            transaction_data["merchant_name"],
            transaction_data["notes"],
            transaction_data["tags"],
            transaction_data["is_recurring"],
            transaction_data["created_at"],
            transaction_data["updated_at"]
        ))
        
        return Transaction(
            id=transaction_id,
            user_id=transaction.user_id,
            amount=transaction.amount,
            description=transaction.description,
            category=transaction.category,
            transaction_type=transaction.transaction_type,
            date=transaction.date,
            source=transaction.source,
            account_id=transaction.account_id,
            merchant_name=transaction.merchant_name,
            notes=transaction.notes,
            tags=transaction.tags,
            is_recurring=transaction.is_recurring,
            created_at=now,
            updated_at=now
        )
    
    async def get_transaction(self, transaction_id: str) -> Optional[Dict[str, Any]]:
        # Optimized query - select only needed columns
        query = "SELECT id, user_id, amount, description, category, transaction_type, date, source, created_at, updated_at FROM transactions WHERE id = ?"
        result = db_client.fetch_one(query, (transaction_id,))
        return dict(result) if result else None
    
    async def update_transaction(self, transaction_id: str, transaction: TransactionUpdate) -> bool:
        update_fields = []
        params = []
        
        if transaction.category is not None:
            update_fields.append("category = ?")
            params.append(transaction.category.value if hasattr(transaction.category, 'value') else transaction.category)
        if transaction.description is not None:
            update_fields.append("description = ?")
            params.append(transaction.description)
        if transaction.notes is not None:
            update_fields.append("notes = ?")
            params.append(transaction.notes)
        if transaction.tags is not None:
            update_fields.append("tags = ?")
            params.append(",".join(transaction.tags))
        if transaction.is_recurring is not None:
            update_fields.append("is_recurring = ?")
            params.append(1 if transaction.is_recurring else 0)
        
        if update_fields:
            update_fields.append("updated_at = ?")
            params.append(datetime.utcnow().isoformat())
            params.append(transaction_id)
            
            query = f"UPDATE transactions SET {', '.join(update_fields)} WHERE id = ?"
            db_client.execute_query(query, tuple(params))
            return True
        return True
    
    async def delete_transaction(self, transaction_id: str) -> bool:
        query = "DELETE FROM transactions WHERE id = ?"
        cursor = db_client.execute_query(query, (transaction_id,))
        return cursor.rowcount > 0
    
    async def get_user_transactions(
        self, 
        user_id: str, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        category: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        # Optimized query with proper indexing
        query = "SELECT id, amount, description, category, transaction_type, date FROM transactions WHERE user_id = ?"
        params = [user_id]
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date.isoformat())
        if end_date:
            query += " AND date <= ?"
            params.append(end_date.isoformat())
        if category:
            query += " AND category = ?"
            params.append(category)
        
        query += " ORDER BY date DESC LIMIT ?"
        params.append(limit)
        
        results = db_client.fetch_all(query, tuple(params))
        return [dict(row) for row in results]
    
    async def get_summary(self, user_id: str, period: str = 'month') -> Dict[str, Any]:
        # Optimized summary query - single query instead of multiple
        end_date = datetime.now()
        if period == 'week':
            start_date = end_date - timedelta(days=7)
        elif period == 'year':
            start_date = end_date - timedelta(days=365)
        else:
            start_date = end_date - timedelta(days=30)
        
        query = """
            SELECT 
                COALESCE(SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END), 0) as total_income,
                COALESCE(SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END), 0) as total_expense,
                COUNT(*) as transaction_count
            FROM transactions 
            WHERE user_id = ? AND date >= ? AND date <= ?
        """
        result = db_client.fetch_one(query, (user_id, start_date.isoformat(), end_date.isoformat()))
        
        return {
            "total_income": result['total_income'] if result else 0,
            "total_expenses": result['total_expense'] if result else 0,
            "net_savings": (result['total_income'] - result['total_expense']) if result else 0,
            "transaction_count": result['transaction_count'] if result else 0,
            "period_start": start_date,
            "period_end": end_date
        }
