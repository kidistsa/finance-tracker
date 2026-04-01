import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

# Database path for SQLite
DB_PATH = Path(__file__).parent.parent.parent / "finance.db"

class SQLiteClient:
    def __init__(self):
        self.db_path = DB_PATH
        self._init_db()
        print(f"✅ SQLite database initialized at {self.db_path}")
    
    def _init_db(self):
        """Create tables if they don't exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    hashed_password TEXT NOT NULL,
                    full_name TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Transactions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    amount REAL NOT NULL,
                    description TEXT NOT NULL,
                    category TEXT NOT NULL,
                    transaction_type TEXT NOT NULL,
                    date TEXT NOT NULL,
                    source TEXT DEFAULT 'manual',
                    account_id TEXT,
                    merchant_name TEXT,
                    notes TEXT,
                    tags TEXT,
                    is_recurring INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            ''')
            
            # Budgets table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS budgets (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    month TEXT NOT NULL,
                    notification_threshold REAL DEFAULT 80,
                    rollover_enabled INTEGER DEFAULT 0,
                    spent REAL DEFAULT 0,
                    remaining REAL DEFAULT 0,
                    percentage_used REAL DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            ''')
            
            # Create indexes
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_budgets_user_id ON budgets(user_id)')
            
            conn.commit()
            print("✅ Tables created/verified successfully")
    
    @contextmanager
    def get_connection(self):
        """Get a database connection with context manager"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: tuple = ()):
        """Execute a single query"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor
    
    def fetch_all(self, query: str, params: tuple = ()):
        """Fetch all results from a query"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def fetch_one(self, query: str, params: tuple = ()):
        """Fetch a single result from a query"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()

# Create a singleton instance
db_client = SQLiteClient()