import sqlite3
import random
from datetime import datetime, timedelta

# Connect to SQLite database
conn = sqlite3.connect('employee.db')
cursor = conn.cursor()

# Recreate employee table (drop old if needed)
cursor.execute("DROP TABLE IF EXISTS employee")

# Create new schema
cursor.execute('''
CREATE TABLE IF NOT EXISTS employee (
    emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    dob DATE,               -- Nullable
    user_type INTEGER NOT NULL
)
''')

# Dummy name pool
first_names = ['John', 'Jane', 'Alex', 'Emily', 'Chris', 'Katie', 'Mike', 'Laura', 'David', 'Sarah']
last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Martinez', 'Lee']

def random_date(start_year=1970, end_year=2000):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    return (start + timedelta(days=random.randint(0, delta.days))).strftime('%Y-%m-%d')

# Insert 50 dummy records
for _ in range(50):
    full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
    dob = random_date() if random.random() > 0.1 else None  # 10% chance dob is NULL
    user_type = random.randint(1, 5)  # Example range of user types
    cursor.execute('''
        INSERT INTO employee (name, dob, user_type)
        VALUES (?, ?, ?)
    ''', (full_name, dob, user_type))

conn.commit()
conn.close()
