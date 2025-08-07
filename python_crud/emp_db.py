import sqlite3
from datetime import date  # Required for type hinting and clarity

DB_FILE = "employee.db"

def search_employees(name="", dob=None, user_type=None):
    """Search employees based on optional filters."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    query = "SELECT emp_id, name, dob, user_type FROM employee WHERE 1=1"
    params = []

    if name:
        query += " AND name LIKE ?"
        params.append(f"%{name}%")
    
    if dob:
        query += " AND DATE(dob) = ?"
        params.append(dob.isoformat() if isinstance(dob, date) else dob)

    if user_type not in (None, ""):
        try:
            user_type_int = int(user_type)
            query += " AND user_type = ?"
            params.append(user_type_int)
        except ValueError:
            return []  # Invalid user_type; return nothing

    try:
        results = cursor.execute(query, params).fetchall()
        return results
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        conn.close()


def insert_employee(name: str, dob: date, user_type: int):
    """Insert a new employee record."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO employee (name, dob, user_type) VALUES (?, ?, ?)",
            (name, dob.isoformat(), user_type),
        )
        conn.commit()
        return None
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        conn.close()


def update_employee(emp_id: int, name: str, dob: date, user_type: int):
    """Update an existing employee record."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE employee
            SET name = ?, dob = ?, user_type = ?
            WHERE emp_id = ?
            """,
            (name, dob.isoformat(), user_type, emp_id),
        )
        conn.commit()
        return None
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        conn.close()
