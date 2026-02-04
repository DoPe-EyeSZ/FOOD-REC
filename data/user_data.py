
#Creating table
def create_user_table(connection):
    query = '''
        CREATE TABLE IF NOT EXISTS users(
            user_id TEXT PRIMARY KEY,
            name TEXT,
            password TEXT
        )
    '''

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()

    except Exception as e:
        print(f"create_user_table has an error: {e}")