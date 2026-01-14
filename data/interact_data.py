import sqlite3


#Creating table
def create_interact_table(connection):
    query = '''
        CREATE TABLE IF NOT EXISTS interactions(
            id INTEGER PRIMARY KEY,
            place_id INTEGER,
            rating REAL,
            rating_count INTEGER,
            is_open INTEGER CHECK (is_open IN (0, 1)),
            drive_time INTEGER,
            accepted INTEGER DEFAULT 0 CHECK(accepted IN (0, 1))

        )
    '''

    try:
        with connection:
            connection.execute(query)

    except Exception as e:
        print(f"create_interact_table has an error: {e}")


#Inserting interaction
def insert_interaction(connection, place_id, rating, rating_count, is_open, drive_time):
    query = "INSERT INTO interactions (place_id, rating, rating_count, is_open, drive_time) VALUES (?, ?, ?, ?, ?)"

    try:
        with connection:
            connection.execute(query, (place_id, rating, rating_count, is_open, drive_time))

    except Exception as e:
        print(f"insert_interaction has an error: {e}")


#Deleting interaction
def delete_interaction(connection, id):
    query = "DELETE FROM interactions WHERE id = ?"

    try:
        with connection:
            connection.execute(query, (id,))

    except Exception as e:
        print(f"delete_interaction has an error: {e}")


def delete_interactions(connection):
    query = "DELETE FROM interactions"

    try:
        with connection:
            connection.execute(query)
    
    except Exception as e:
        print(f"delete_interactions has an error: {e}")


#THINGS TO WORK ON
'''
1. updating user decision
2. implement the sql to api
3. split process of data gathers ----> data refine/traingin
'''