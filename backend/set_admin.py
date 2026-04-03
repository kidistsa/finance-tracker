import sqlite3

conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

email = 'kidipassion4@gmail.com'
cursor.execute("UPDATE users SET role = 'admin' WHERE email = ?", (email,))
conn.commit()

if cursor.rowcount > 0:
    print(f'✅ {email} is now an ADMIN!')
else:
    print(f'❌ {email} not found')

# Verify
cursor.execute("SELECT email, role FROM users WHERE email = ?", (email,))
user = cursor.fetchone()
if user:
    print(f'📋 {user[0]} -> Role: {user[1]}')

conn.close()
