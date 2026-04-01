import sqlite3

conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

# Drop if exists (clean slate)
cursor.execute("DROP TABLE IF EXISTS budgets")
print("✅ Dropped old budgets table")

# Create new budgets table
cursor.execute('''
    CREATE TABLE budgets (
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
print("✅ Created budgets table")

# Create indexes
cursor.execute('CREATE INDEX idx_budgets_user_id ON budgets(user_id)')
cursor.execute('CREATE INDEX idx_budgets_month ON budgets(month)')
print("✅ Created indexes")

conn.commit()
conn.close()

print("\n🎉 Budgets table created successfully!")