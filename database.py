import sqlite3

conn = sqlite3.connect("greenstride.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS activities(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activity_name TEXT,
    description TEXT,
    activity_date TEXT,
    eco_points INTEGER
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")