import logging
import json
from datetime import datetime
from typing import Any, Dict
from app.core.db import db_client
import asyncio

# Configure JSON logging
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if hasattr(record, 'user_id'):
            log_entry["user_id"] = record.user_id
        if hasattr(record, 'request_id'):
            log_entry["request_id"] = record.request_id
        
        return json.dumps(log_entry)


# Setup logging
logger = logging.getLogger("finance_tracker")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(JSONFormatter())
logger.addHandler(console_handler)


class AuditLogger:
    @staticmethod
    async def log_action_async(user_id: str, action: str, details: Dict[str, Any] = None, ip_address: str = None):
        # Async version - non-blocking
        try:
            query = """
                INSERT INTO audit_logs (user_id, action, details, ip_address, created_at)
                VALUES (?, ?, ?, ?, ?)
            """
            
            db_client.execute_query(query, (
                user_id,
                action,
                json.dumps(details) if details else None,
                ip_address,
                datetime.utcnow().isoformat()
            ))
            
            # Also log to file (non-blocking)
            logger.info(
                f"Audit: User {user_id} performed {action}",
                extra={"user_id": user_id, "action": action, "details": details}
            )
        except Exception as e:
            # Don't let audit logging break the main flow
            print(f"Audit log error: {e}")
    
    @staticmethod
    def log_action(user_id: str, action: str, details: Dict[str, Any] = None, ip_address: str = None):
        # Sync version - runs in background
        try:
            query = """
                INSERT INTO audit_logs (user_id, action, details, ip_address, created_at)
                VALUES (?, ?, ?, ?, ?)
            """
            
            db_client.execute_query(query, (
                user_id,
                action,
                json.dumps(details) if details else None,
                ip_address,
                datetime.utcnow().isoformat()
            ))
        except Exception as e:
            print(f"Audit log error: {e}")
    
    @staticmethod
    async def log_login_async(user_id: str, success: bool, ip_address: str = None):
        # Async login logging
        action = "login_success" if success else "login_failed"
        details = {"ip": ip_address, "success": success}
        await AuditLogger.log_action_async(user_id, action, details, ip_address)
    
    @staticmethod
    def log_login(user_id: str, success: bool, ip_address: str = None):
        # Sync login logging
        action = "login_success" if success else "login_failed"
        details = {"ip": ip_address, "success": success}
        AuditLogger.log_action(user_id, action, details, ip_address)
    
    @staticmethod
    async def get_user_audit_logs(user_id: str, limit: int = 50) -> list:
        query = """
            SELECT action, details, ip_address, created_at
            FROM audit_logs
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """
        results = db_client.fetch_all(query, (user_id, limit))
        return [dict(row) for row in results]
