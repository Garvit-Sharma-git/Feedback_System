import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE feedbacks ADD COLUMN employee_comment TEXT;")
    print("✅ Column added successfully.")
except sqlite3.OperationalError as e:
    print(f"⚠️ Skipped: {e}")  # Likely means column already exists

conn.commit()
conn.close()
