import secrets
from datetime import datetime, timedelta
from app.core.db import db_client

class SessionManager:
    @staticmethod
    def create_session(user_id: str) -> str:
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(days=7)
        
        query = """
            INSERT INTO sessions (session_token, user_id, expires_at, created_at)
            VALUES (?, ?, ?, ?)
        """
        db_client.execute_query(query, (
            session_token,
            user_id,
            expires_at.isoformat(),
            datetime.utcnow().isoformat()
        ))
        
        return session_token
    
    @staticmethod
    def validate_session(session_token: str) -> bool:
        query = """
            SELECT user_id FROM sessions 
            WHERE session_token = ? AND expires_at > ? AND is_active = 1
        """
        result = db_client.fetch_one(query, (session_token, datetime.utcnow().isoformat()))
        return result is not None
    
    @staticmethod
    def revoke_session(session_token: str):
        query = "UPDATE sessions SET is_active = 0 WHERE session_token = ?"
        db_client.execute_query(query, (session_token,))
    
    @staticmethod
    def revoke_all_user_sessions(user_id: str):
        query = "UPDATE sessions SET is_active = 0 WHERE user_id = ?"
        db_client.execute_query(query, (user_id,))
