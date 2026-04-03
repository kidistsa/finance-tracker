import sqlite3

conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

# Add email verification and password reset columns
try:
    cursor.execute("ALTER TABLE users ADD COLUMN email_verified INTEGER DEFAULT 0")
    print("? Added email_verified column")
except sqlite3.OperationalError:
    print("?? email_verified already exists")

try:
    cursor.execute("ALTER TABLE users ADD COLUMN verification_token TEXT")
    print("? Added verification_token column")
except sqlite3.OperationalError:
    print("?? verification_token already exists")

try:
    cursor.execute("ALTER TABLE users ADD COLUMN reset_token TEXT")
    print("? Added reset_token column")
except sqlite3.OperationalError:
    print("?? reset_token already exists")

try:
    cursor.execute("ALTER TABLE users ADD COLUMN reset_token_expires TEXT")
    print("? Added reset_token_expires column")
except sqlite3.OperationalError:
    print("?? reset_token_expires already exists")

conn.commit()
conn.close()
print("\n?? Database updated for email verification and password reset!")
