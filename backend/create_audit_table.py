import sqlite3

conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

# Create audit logs table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        action TEXT NOT NULL,
        details TEXT,
        ip_address TEXT,
        created_at TEXT NOT NULL
    )
''')

# Create indexes for faster queries
cursor.execute('CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_logs(user_id)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_logs(action)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_logs(created_at)')

conn.commit()
conn.close()

print("✅ Audit logs table created successfully!")
