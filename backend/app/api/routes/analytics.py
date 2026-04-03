from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from app.api.dependencies.auth import get_current_user
from app.core.db import db_client

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/monthly-comparison")
async def get_monthly_comparison(
    months: int = 6,
    current_user: dict = Depends(get_current_user)
):
    monthly_data = []
    
    for i in range(months - 1, -1, -1):
        date = datetime.now() - timedelta(days=30 * i)
        month_start = date.replace(day=1).strftime('%Y-%m-%d')
        
        if date.month == 12:
            month_end = date.replace(year=date.year + 1, month=1, day=1).strftime('%Y-%m-%d')
        else:
            month_end = date.replace(month=date.month + 1, day=1).strftime('%Y-%m-%d')
        
        query = """
            SELECT 
                COALESCE(SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END), 0) as income,
                COALESCE(SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END), 0) as expense
            FROM transactions 
            WHERE user_id = ? AND date >= ? AND date < ?
        """
        row = db_client.fetch_one(query, (current_user["email"], month_start, month_end))
        
        monthly_data.append({
            "month": date.strftime('%b %Y'),
            "income": row['income'] if row else 0,
            "expense": row['expense'] if row else 0,
            "savings": (row['income'] if row else 0) - (row['expense'] if row else 0)
        })
    
    return monthly_data
