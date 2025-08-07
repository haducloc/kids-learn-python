import sqlite3
from datetime import date

DB_FILE = "employee.db"


def search_employees(
    name: str | None = None, dob: date | None = None, user_type: int | None = None
):
    """Search employees based on filters."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    query = "SELECT emp_id, name, dob, user_type FROM employee WHERE 1=1"
    params = []

    if name is not None:
        query += " AND name LIKE ?"
        params.append(f"%{name}%")

    if dob is not None:
        query += " AND DATE(dob) = ?"
        params.append(dob.isoformat())

    if user_type is not None:
        query += " AND user_type = ?"
        params.append(user_type)

    try:
        results = cursor.execute(query, params).fetchall()
        return results
    except Exception as e:
        return [("Error", str(e))]
    finally:
        cursor.close()
        conn.close()


def insert_employee(name: str, dob: date | None, user_type: int):
    """Insert a new employee record."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # SQLite does not support Date type directly, so we store it as text
        # Convert date to YYYY-MM-DD format
        date_str = dob.strftime("%Y-%m-%d") if isinstance(dob, date) else None

        cursor.execute(
            "INSERT INTO employee (name, dob, user_type) VALUES (?, ?, ?)",
            (name, date_str, user_type),
        )
        conn.commit()
        return None
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        conn.close()


def update_employee(emp_id: int, name: str, dob: date | None, user_type: int):
    """Update an existing employee record."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        date_str = dob.strftime("%Y-%m-%d") if isinstance(dob, date) else None
        
        cursor.execute(
            """
            UPDATE employee
            SET name = ?, dob = ?, user_type = ?
            WHERE emp_id = ?
            """,
            (name, date_str, user_type, emp_id),
        )
        conn.commit()
        return None
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        conn.close()
