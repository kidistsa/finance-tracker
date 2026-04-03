import sqlite3

conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

# Add indexes to speed up queries
print("Adding database indexes for better performance...")

# Index for audit_logs table
cursor.execute('CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs(action)')

# Index for users table
cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)')

# Index for transactions table
cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_user_date ON transactions(user_id, date)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(transaction_type)')

conn.commit()
conn.close()

print("✅ Database indexes added successfully!")
