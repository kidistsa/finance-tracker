import sqlite3

conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

# Update user to admin
email = 'kidipassion4@gmail.com'
cursor.execute('UPDATE users SET role = ? WHERE email = ?', ('admin', email))
conn.commit()

if cursor.rowcount > 0:
    print(f'✅ User {email} is now an ADMIN!')
else:
    print(f'❌ User {email} not found')

# Verify
cursor.execute('SELECT email, role FROM users WHERE email = ?', (email,))
user = cursor.fetchone()
if user:
    print(f'📋 {user[0]} -> Role: {user[1]}')

conn.close()
