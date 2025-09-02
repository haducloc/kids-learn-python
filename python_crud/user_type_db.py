import sqlite3

DB_FILE = "employee.db"

def list_user_types():
    """
    Retrieves all user types from the user_types table.
    Returns a list of tuples containing user_type and name.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        query = "SELECT user_type, name FROM user_types"
        results = cursor.execute(query).fetchall()
        return results
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        conn.close()
