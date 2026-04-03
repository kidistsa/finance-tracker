import sqlite3

conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

print("🔧 Adding database indexes for better performance...")

# Users table indexes
cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)')
print("✅ Users table indexes added")

# Transactions table indexes
cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_user_date ON transactions(user_id, date)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(transaction_type)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_category ON transactions(category)')
print("✅ Transactions table indexes added")

# Budgets table indexes
cursor.execute('CREATE INDEX IF NOT EXISTS idx_budgets_user_month ON budgets(user_id, month)')
print("✅ Budgets table indexes added")

# Audit logs table indexes
cursor.execute('CREATE INDEX IF NOT EXISTS idx_audit_user_action ON audit_logs(user_id, action)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_logs(created_at)')
print("✅ Audit logs table indexes added")

conn.commit()
conn.close()

print("🎉 All database indexes added successfully!")
