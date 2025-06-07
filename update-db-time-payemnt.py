import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "stripe/stripe_test.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 🏷 Add payment_date column if not exists
try:
    cursor.execute("ALTER TABLE payments ADD COLUMN payment_date TEXT")
    print("✅ Added 'payment_date' column.")
except sqlite3.OperationalError as e:
    if "duplicate column" in str(e).lower():
        print("⚠️ Column 'payment_date' already exists, skipping.")
    else:
        raise

# 🎲 Generate and update random dates within the last 60 days
cursor.execute("SELECT id FROM payments")
payments = cursor.fetchall()

for (pid,) in payments:
    random_days_ago = random.randint(0, 59)
    random_datetime = datetime.now() - timedelta(days=random_days_ago)
    iso_date = random_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    cursor.execute("UPDATE payments SET payment_date = ? WHERE id = ?", (iso_date, pid))

conn.commit()
conn.close()
print("✅ Randomized payment dates updated.")
