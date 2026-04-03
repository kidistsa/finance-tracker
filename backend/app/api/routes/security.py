from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from app.api.dependencies.auth import require_admin, get_current_user
from app.core.db import db_client
import json

router = APIRouter(prefix="/security", tags=["Security"])


@router.get("/audit-logs")
async def get_audit_logs(
    current_user: dict = Depends(require_admin),
    limit: int = 100
) -> List[Dict[str, Any]]:
    # ADMIN ONLY - Get all audit logs
    query = """
        SELECT user_id, action, details, ip_address, created_at
        FROM audit_logs
        ORDER BY created_at DESC
        LIMIT ?
    """
    results = db_client.fetch_all(query, (limit,))
    logs = []
    
    for row in results:
        details = {}
        if row['details']:
            try:
                details = json.loads(row['details'])
            except:
                details = {"raw": row['details']}
        
        logs.append({
            "user_id": row['user_id'],
            "action": row['action'],
            "details": details,
            "ip_address": row['ip_address'],
            "created_at": row['created_at']
        })
    
    return logs


@router.get("/my-logs")
async def get_my_audit_logs(
    current_user: dict = Depends(get_current_user),
    limit: int = 50
) -> List[Dict[str, Any]]:
    # ANY USER - Get only their own logs
    query = """
        SELECT action, details, ip_address, created_at
        FROM audit_logs
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    """
    results = db_client.fetch_all(query, (current_user["email"], limit))
    logs = []
    
    for row in results:
        details = {}
        if row['details']:
            try:
                details = json.loads(row['details'])
            except:
                details = {"raw": row['details']}
        
        logs.append({
            "action": row['action'],
            "details": details,
            "ip_address": row['ip_address'],
            "created_at": row['created_at']
        })
    
    return logs
