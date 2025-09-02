import sqlite3
import random
from datetime import datetime, timedelta

# Connect to SQLite database
conn = sqlite3.connect('employee.db')
cursor = conn.cursor()

# Drop and recreate employee table
cursor.execute("DROP TABLE IF EXISTS employee")
cursor.execute('''
CREATE TABLE IF NOT EXISTS employee (
    emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    dob DATE,               -- Nullable
    user_type INTEGER NOT NULL
)
''')

# Sample name pool for generating random names
first_names = ['John', 'Jane', 'Alex', 'Emily', 'Chris', 'Katie', 'Mike', 'Laura', 'David', 'Sarah']
last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Martinez', 'Lee']

# Generate a random birth date between two years
def random_date(start_year=1970, end_year=2000):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    return (start + timedelta(days=random.randint(0, delta.days))).strftime('%Y-%m-%d')

# Insert 50 dummy employees
for _ in range(50):
    full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
    dob = random_date() if random.random() > 0.1 else None  # 10% chance dob is NULL
    user_type = random.randint(1, 5)  # User type code between 1–5
    cursor.execute('''
        INSERT INTO employee (name, dob, user_type)
        VALUES (?, ?, ?)
    ''', (full_name, dob, user_type))

# Drop and recreate user_types table with fixed codes
cursor.execute("DROP TABLE IF EXISTS user_types")
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_types (
    user_type INTEGER PRIMARY KEY,  -- Fixed codes (1–5)
    name TEXT NOT NULL
)
''')

# Insert predefined user type codes and names
coded_user_types = {
    1: "Administrator",
    2: "Manager",
    3: "HR",
    4: "Engineer",
    5: "Intern"
}

for code, name in coded_user_types.items():
    cursor.execute("INSERT INTO user_types (user_type, name) VALUES (?, ?)", (code, name))

# Finalize changes and close connection
conn.commit()
conn.close()
