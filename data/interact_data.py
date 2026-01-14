import sqlite3


def create_interact_table(connection):
    query = '''
        CREATE TABLE IF NOT EXISTS interactions(
            id INTEGER PRIMARY KEY,
            place_id INTEGER,
            rating REAL,
            rating_count INTEGER,
            is_open INTEGER CHECK (is_open IN (0, 1)),
            drive_time INTEGER

        )
    '''

    try:
        with connection:
            connection.execute(query)

    except Exception as e:
        print(f"create_interact_table has an error: {e}")