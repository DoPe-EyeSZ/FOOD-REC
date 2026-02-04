#Creating table
# USEthisLATERUSEthisLATERUSEthisLATERUSEthisLATERUSEthisLATER FOREIGN KEY (user_id) REFERENCES users(user_id)
def create_interact_table(connection):
    query = '''
        CREATE TABLE IF NOT EXISTS user_interactions(
            id SERIAL PRIMARY KEY,
            user_id TEXT DEFAULT 'test_user',
            place_id TEXT,
            rating REAL,
            rating_count INTEGER,
            is_open INTEGER CHECK (is_open IN (0, 1)),
            drive_time INTEGER,
            accepted INTEGER CHECK(accepted IN (0, 1)),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (place_id) REFERENCES restaurants(place_id)
    
        )
    '''

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()

    except Exception as e:
        print(f"create_user_interact_table has an error: {e}")


#Inserting interaction
def insert_user_interaction(connection, place_id, rating, rating_count, is_open, drive_time, accepted, user_id = 'test_user'):
    query = '''
    INSERT INTO user_interactions (user_id, place_id, rating, rating_count, is_open, drive_time, accepted) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''

    try:
        cursor = connection.cursor()
        cursor.execute(query, (user_id, place_id, rating, rating_count, is_open, drive_time, accepted))
        connection.commit()
        cursor.close()

    except Exception as e:
        print(f"insert_interaction has an error: {e}")


#Deleting interaction
def delete_user_interaction(connection, id):
    query = "DELETE FROM user_interactions WHERE id = %s"

    try:
        cursor = connection.cursor()
        cursor.execute(query, (id,))
        connection.commit()
        cursor.close()
        

    except Exception as e:
        print(f"delete_user_interaction has an error: {e}")


def delete_user_interactions(connection, user_id = 'test_user'):
    query = "DELETE FROM user_interactions WHERE user_id = %s"

    try:
        cursor = connection.cursor()
        cursor.execute(query, (user_id,))
        connection.commit()
        cursor.close()
        print('success')
    
    except Exception as e:
        print(f"delete_user_interactions has an error: {e}")


#Fetching data
def fetch_user_interaction(connection, id, user_id = "test_user"):
    query = "SELECT * FROM user_interactions WHERE id = %s AND user_id = %s"

    try:
        cursor = connection.cursor()
        cursor.execute(query, (id, user_id))
        data = cursor.fetchone()
        cursor.close()
        return data
        
    except Exception as e:
        print(f"fetch_user_interaction has an error: {e}")


def fetch_user_interactions(connection, user_id = "test_user"):
    query = "SELECT * FROM user_interactions WHERE user_id = %s"

    try:
            
        cursor = connection.cursor()
        cursor.execute(query, (user_id,))
        data = cursor.fetchall()
        cursor.close()
        return data
            
    
    except Exception as e:
        print(f"fetch_interactions has an error: {e}")

