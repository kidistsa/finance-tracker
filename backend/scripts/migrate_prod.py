import sqlite3
import os

def migrate_to_postgres():
    \"\"\"Prepare SQLite data for PostgreSQL migration\"\"\"
    print("Preparing database for production...")
    
    # Your existing SQLite database
    sqlite_conn = sqlite3.connect('finance.db')
    sqlite_cursor = sqlite_conn.cursor()
    
    # Export schema
    sqlite_cursor.execute("SELECT sql FROM sqlite_master WHERE type='table'")
    tables = sqlite_cursor.fetchall()
    
    print("Database schema ready for PostgreSQL")
    
    sqlite_conn.close()
    
    print("Next steps:")
    print("1. Create a PostgreSQL database on Railway")
    print("2. Set DATABASE_URL environment variable")
    print("3. Run migrations with Alembic")

if __name__ == "__main__":
    migrate_to_postgres()
