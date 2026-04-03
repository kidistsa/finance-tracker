from datetime import datetime, timedelta
from app.repositories.user_repo import UserRepository
from app.repositories.transaction_repo import TransactionRepository


class AdminService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.tx_repo = TransactionRepository()
    
    async def get_user_growth(self, days: int = 30) -> list:
        # Get user registration growth over time
        growth = []
        for i in range(days, -1, -1):
            date = datetime.now() - timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            growth.append({'date': date_str, 'users': 0})
        return growth
    
    async def get_system_stats(self):
        # Get system-wide statistics
        total_users = await self.user_repo.count_users()
        active_users = await self.user_repo.count_users("active")
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'total_transactions': 0
        }
