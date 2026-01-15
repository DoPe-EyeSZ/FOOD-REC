import sqlite3

#Creating table
def create_user_table(connection):
    query = '''
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            PASSWORD TEXT
        )
    '''

    try:
        with connection:
            connection.execute(query)

    except Exception as e:
        print(f"create_user_table has an error: {e}")