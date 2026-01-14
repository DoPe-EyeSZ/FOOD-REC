import sqlite3

def get_connection(db_name):
    try:
        path = "instance/" + db_name
        return sqlite3.connect(path)
    except Exception as e:
        print(f"Error: {e}")