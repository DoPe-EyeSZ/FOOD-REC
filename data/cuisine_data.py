import sqlite3

def get_connection(db_name):
    try:
        path = "instance/" + db_name
        return sqlite3.connect(path)
    except Exception as e:
        print(f"Error: {e}")

#Creating separate multiple tables
def create_cuisine_table(connection):
    query = f'''
        CREATE TABLE IF NOT EXISTS cuisine(
            id INTEGER PRIMARY KEY,
            cuisine TEXT,
            shown INTEGER,
            accepted INTEGER

        )
    '''
    try:
        with connection:
            connection.execute(query)
    except Exception as e:
        print(f"Error: {e}")
