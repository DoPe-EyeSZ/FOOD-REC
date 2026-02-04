
#Creating table
def create_user_table(connection):
    query = '''
        CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            name TEXT,
            password_hash TEXT NOT NULL
        )
    '''

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()

    except Exception as e:
        print(f"create_user_table has an error: {e}")