import sqlite3
import os

# Connect to SQLite database (creates it if it doesn't exist)
conn = sqlite3.connect('example.db')

# Create a cursor object
cur = conn.cursor()

# 1. Create a table
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER
    )
''')

# 2. Insert data
cur.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Alice', 30))
cur.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Bob', 25))
conn.commit()  # Commit the transaction

# 3. Query data
cur.execute("SELECT * FROM users")
rows = cur.fetchall()
print("All Users:")
for row in rows:
    print(row)

# 4. Update a record
cur.execute("UPDATE users SET age = ? WHERE name = ?", (31, 'Alice'))
conn.commit()

# 5. Delete a record
cur.execute("DELETE FROM users WHERE name = ?", ('Bob',))
conn.commit()

# Show final state
cur.execute("SELECT * FROM users")
print("\nAfter Update and Delete:")
for row in cur.fetchall():
    print(row)

# Close the cursor
cur.close();

# Close the connection
conn.close()

# Remove db
os.remove('example.db')