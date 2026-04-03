import sqlite3

conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

# Add new columns if they don't exist
try:
    cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
    print("✅ Added role column")
except sqlite3.OperationalError:
    print("⚠️ role column already exists")

try:
    cursor.execute("ALTER TABLE users ADD COLUMN status TEXT DEFAULT 'active'")
    print("✅ Added status column")
except sqlite3.OperationalError:
    print("⚠️ status column already exists")

try:
    cursor.execute("ALTER TABLE users ADD COLUMN is_verified INTEGER DEFAULT 0")
    print("✅ Added is_verified column")
except sqlite3.OperationalError:
    print("⚠️ is_verified column already exists")

try:
    cursor.execute("ALTER TABLE users ADD COLUMN updated_at TIMESTAMP")
    print("✅ Added updated_at column")
except sqlite3.OperationalError:
    print("⚠️ updated_at column already exists")

try:
    cursor.execute("ALTER TABLE users ADD COLUMN last_login TIMESTAMP")
    print("✅ Added last_login column")
except sqlite3.OperationalError:
    print("⚠️ last_login column already exists")

# Update existing users to have default values
cursor.execute("UPDATE users SET role = 'user' WHERE role IS NULL")
cursor.execute("UPDATE users SET status = 'active' WHERE status IS NULL")
cursor.execute("UPDATE users SET is_verified = 1 WHERE is_verified IS NULL")

conn.commit()
conn.close()
print("\n🎉 User table updated successfully!")
