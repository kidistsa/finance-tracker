import sqlite3

# Connect to your database
conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

print("🔄 Updating database...")

# Drop old transactions table
cursor.execute("DROP TABLE IF EXISTS transactions")
print("✅ Removed old table")

# Create new transactions table
cursor.execute('''
    CREATE TABLE transactions (
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
print("✅ Created new table")

# Create indexes
cursor.execute("CREATE INDEX idx_transactions_user_id ON transactions(user_id)")
cursor.execute("CREATE INDEX idx_transactions_date ON transactions(date)")
print("✅ Created indexes")

conn.commit()
conn.close()

print("\n🎉 DATABASE FIXED! Now restart your server and try uploading the CSV.")