import sqlite3

conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

# Create sessions table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_token TEXT UNIQUE NOT NULL,
        user_id TEXT NOT NULL,
        expires_at TEXT NOT NULL,
        is_active INTEGER DEFAULT 1,
        created_at TEXT NOT NULL
    )
''')

# Create index
cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(session_token)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id)')

conn.commit()
conn.close()

print("✅ Sessions table created successfully!")
