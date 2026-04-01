import sqlite3

conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

# Check current columns
cursor.execute("PRAGMA table_info(budgets)")
columns = cursor.fetchall()
print("Current columns:")
for col in columns:
    print(f"  - {col[1]}")

# Add missing columns if they don't exist
try:
    cursor.execute("ALTER TABLE budgets ADD COLUMN notification_threshold REAL DEFAULT 80")
    print("✅ Added notification_threshold column")
except sqlite3.OperationalError:
    print("⚠️ notification_threshold column already exists")

try:
    cursor.execute("ALTER TABLE budgets ADD COLUMN rollover_enabled INTEGER DEFAULT 0")
    print("✅ Added rollover_enabled column")
except sqlite3.OperationalError:
    print("⚠️ rollover_enabled column already exists")

try:
    cursor.execute("ALTER TABLE budgets ADD COLUMN spent REAL DEFAULT 0")
    print("✅ Added spent column")
except sqlite3.OperationalError:
    print("⚠️ spent column already exists")

try:
    cursor.execute("ALTER TABLE budgets ADD COLUMN remaining REAL DEFAULT 0")
    print("✅ Added remaining column")
except sqlite3.OperationalError:
    print("⚠️ remaining column already exists")

try:
    cursor.execute("ALTER TABLE budgets ADD COLUMN percentage_used REAL DEFAULT 0")
    print("✅ Added percentage_used column")
except sqlite3.OperationalError:
    print("⚠️ percentage_used column already exists")

try:
    cursor.execute("ALTER TABLE budgets ADD COLUMN created_at TEXT")
    print("✅ Added created_at column")
except sqlite3.OperationalError:
    print("⚠️ created_at column already exists")

try:
    cursor.execute("ALTER TABLE budgets ADD COLUMN updated_at TEXT")
    print("✅ Added updated_at column")
except sqlite3.OperationalError:
    print("⚠️ updated_at column already exists")

# Verify new columns
print("\nUpdated columns:")
cursor.execute("PRAGMA table_info(budgets)")
columns = cursor.fetchall()
for col in columns:
    print(f"  ✅ {col[1]} ({col[2]})")

conn.commit()
conn.close()

print("\n🎉 Budgets table updated successfully!")