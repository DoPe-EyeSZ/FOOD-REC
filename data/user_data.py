import sqlite3

#Creating table
def create_user_table(connection):
    query = '''
        CREATE TABLE IF NOT EXISTS users(
            user_id SERIAL PRIMARY KEY,
            name TEXT,
            email TEXT,
            password TEXT
        )
    '''

    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()
            print("user")

    except Exception as e:
        print(f"create_user_table has an error: {e}")