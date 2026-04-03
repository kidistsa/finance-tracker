import sqlite3

# Connect to database
conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

# Count before deletion
cursor.execute("SELECT COUNT(*) FROM recurring_transactions")
count = cursor.fetchone()[0]
print(f"📊 Found {count} recurring transactions")

# Delete all
cursor.execute("DELETE FROM recurring_transactions")
conn.commit()

# Verify deletion
cursor.execute("SELECT COUNT(*) FROM recurring_transactions")
remaining = cursor.fetchone()[0]
print(f"✅ Deleted {count - remaining} transactions")
print(f"📊 Remaining: {remaining}")

conn.close()