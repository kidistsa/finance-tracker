from typing import List, Dict, Any, Optional
from datetime import datetime
from .base import BaseRepository
from app.core.db import db_client


class UserRepository(BaseRepository):
    
    def __init__(self):
        super().__init__("users")
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM users WHERE email = ?"
        result = db_client.fetch_one(query, (email,))
        return dict(result) if result else None
    
    async def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM users WHERE id = ?"
        result = db_client.fetch_one(query, (user_id,))
        return dict(result) if result else None
    
    async def get_all_users(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        query = "SELECT id, email, full_name, role, status, is_verified, created_at, last_login FROM users LIMIT ? OFFSET ?"
        results = db_client.fetch_all(query, (limit, offset))
        return [dict(row) for row in results]
    
    async def update_user(self, user_id: int, update_data: Dict[str, Any]) -> bool:
        update_fields = []
        params = []
        
        for key, value in update_data.items():
            if value is not None:
                update_fields.append(f"{key} = ?")
                params.append(value)
        
        if update_fields:
            update_fields.append("updated_at = ?")
            params.append(datetime.utcnow().isoformat())
            params.append(user_id)
            
            query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"
            db_client.execute_query(query, tuple(params))
            return True
        return True
    
    async def update_last_login(self, user_id: int):
        query = "UPDATE users SET last_login = ? WHERE id = ?"
        db_client.execute_query(query, (datetime.utcnow().isoformat(), user_id))
    
    async def count_users(self, status: Optional[str] = None) -> int:
        if status:
            query = "SELECT COUNT(*) FROM users WHERE status = ?"
            result = db_client.fetch_one(query, (status,))
        else:
            query = "SELECT COUNT(*) FROM users"
            result = db_client.fetch_one(query)
        return result[0] if result else 0
    
    async def delete_user(self, user_id: int) -> bool:
        db_client.execute_query("DELETE FROM transactions WHERE user_id = ?", (str(user_id),))
        query = "DELETE FROM users WHERE id = ?"
        cursor = db_client.execute_query(query, (user_id,))
        return cursor.rowcount > 0
