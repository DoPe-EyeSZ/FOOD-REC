import sqlite3


#Creating table
# USEthisLATERUSEthisLATERUSEthisLATERUSEthisLATERUSEthisLATER FOREIGN KEY (user_id) REFERENCES users(user_id)
def create_interact_table(connection):
    query = '''
        CREATE TABLE IF NOT EXISTS interactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT DEFAULT 'test_user',
            place_id TEXT,
            rating REAL,
            rating_count INTEGER,
            is_open INTEGER CHECK (is_open IN (0, 1)),
            drive_time INTEGER,
            accepted INTEGER DEFAULT 0 CHECK(accepted IN (0, 1)),
            FOREIGN KEY (place_id) REFERENCES restaurants(place_id)
    
        )
    '''

    try:
        with connection:
            connection.execute(query)

    except Exception as e:
        print(f"create_interact_table has an error: {e}")


#Inserting interaction
def insert_interaction(connection, place_id, rating, rating_count, is_open, drive_time, accepted, user_id = 'test_user'):
    query = '''
    INSERT INTO interactions (user_id, place_id, rating, rating_count, is_open, drive_time, accepted) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
    '''

    try:
        with connection:
            connection.execute(query, (user_id, place_id, rating, rating_count, is_open, drive_time, accepted))

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


def delete_interactions(connection, user_id = 'test_user'):
    query = "DELETE FROM interactions WHERE user_id = ?"

    try:
        with connection:
            connection.execute(query, (user_id,))
    
    except Exception as e:
        print(f"delete_interactions has an error: {e}")


#Fetching data
def fetch_interaction(connection, id):
    query = "SELECT * FROM interaction WHERE id = ?"

    try:
        with connection:
            return connection.execute(query, (id))
        
    except Exception as e:
        print(f"fetch_interaction has an error: {e}")


def fetch_interactions(connection):
    query = "SELECT * FROM interactions"

    try:
        with connection:
            return connection.execute(query).fetchall()
            
    
    except Exception as e:
        print(f"fetch_interactions has an error: {e}")

#THINGS TO WORK ON
'''
1. updating user decision
2. implement the sql to api
3. split process of data gathers ----> data refine/traingin
'''