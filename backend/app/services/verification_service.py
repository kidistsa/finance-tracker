import secrets
from datetime import datetime, timedelta
from app.core.db import db_client

class VerificationService:
    
    @staticmethod
    def generate_token():
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def save_verification_token(email, token):
        db_client.execute_query(
            'UPDATE users SET verification_token = ? WHERE email = ?',
            (token, email)
        )
    
    @staticmethod
    def verify_email(token):
        result = db_client.fetch_one(
            'SELECT email FROM users WHERE verification_token = ?',
            (token,)
        )
        if result:
            db_client.execute_query(
                'UPDATE users SET email_verified = 1, verification_token = NULL WHERE verification_token = ?',
                (token,)
            )
            return True
        return False
    
    @staticmethod
    def save_reset_token(email, token):
        expires = (datetime.now() + timedelta(hours=1)).isoformat()
        db_client.execute_query(
            'UPDATE users SET reset_token = ?, reset_token_expires = ? WHERE email = ?',
            (token, expires, email)
        )
    
    @staticmethod
    def verify_reset_token(token):
        result = db_client.fetch_one(
            'SELECT email FROM users WHERE reset_token = ? AND reset_token_expires > ?',
            (token, datetime.now().isoformat())
        )
        return result['email'] if result else None
    
    @staticmethod
    def reset_password(token, new_password):
        from auth import hash_password
        email = VerificationService.verify_reset_token(token)
        if email:
            hashed = hash_password(new_password)
            db_client.execute_query(
                'UPDATE users SET hashed_password = ?, reset_token = NULL, reset_token_expires = NULL WHERE email = ?',
                (hashed, email)
            )
            return True
        return False
