
#Creating Table
def create_cuisine_table(connection):
    query = f'''
        CREATE TABLE IF NOT EXISTS cuisine_stats(
            user_id INTEGER,
            cuisine TEXT,
            shown INTEGER DEFAULT 0,
            accepted INTEGER DEFAULT 0,
            PRIMARY KEY (user_id, cuisine),
            FOREIGN KEY (user_id) REFERENCES users(user_id)

        )
    '''
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()

    except Exception as e:
        print(f"create_cuisine_table has an error: {e}")


#Query through all rows
def fetch_all_cuisine(connection, user_id):
    query = "SELECT * FROM cuisine_stats WHERE user_id = %s"

    try:
        cursor = connection.cursor()
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
        cursor.close()
        return rows
        
    except Exception as e:
        print(f"fetch_all_cuisine has an error: {e}")


#Query for specific cuisine
def fetch_cuisine(connection, cuisine, user_id):
    query = "SELECT * FROM cuisine_stats WHERE user_id = %s AND cuisine = %s"

    try:
            
        cursor = connection.cursor()
        cursor.execute(query, (user_id, cuisine,))
        row = cursor.fetchone()
        cursor.close()

        return row
    
    except Exception as e:
        print(f"fetch_cuisine has an error: {e}")


#Delete row
def delete_cuisine(connection, cuisine, user_id):
    query = "DELETE FROM cuisine_stats WHERE user_id = %s AND cuisine = %s"

    try:
        cursor = connection.cursor()
        cursor.execute(query, (user_id, cuisine,))
        connection.commit()
        cursor.close()
        print('success')
            
    except Exception as e:
        print(f"delete_cuisine has an error: {e}")

def delete_cuisines(connection, user_id):
    query = "DELETE FROM cuisine_stats WHERE user_id = %s"

    try:
        cursor = connection.cursor()
        cursor.execute(query, (user_id,))
        connection.commit()
        cursor.close()
        print('success')
            
    except Exception as e:
        print(f"delete_cuisine has an error: {e}")


#Upsert cuisine information
def upsert_cuisine_stats(connection, cuisine, accepted, user_id):
    query = '''
        INSERT INTO cuisine_stats (user_id, cuisine, shown, accepted)
        VALUES (%s, %s, 1, %s)
        ON CONFLICT(user_id, cuisine)
        DO UPDATE SET
            shown = cuisine_stats.shown + 1,
            accepted = cuisine_stats.accepted + %s
    '''

    try:
        cursor = connection.cursor()
        cursor.execute(query, (user_id, cuisine, accepted, accepted))
        connection.commit()
        cursor.close()

    except Exception as e:
        print(f"upsert_cuisine_stats has an error: {e}")


def increment_acceptance(connection, cuisine, user_id):
    query = '''
        UPDATE cuisine_stats
        SET accepted = accepted + 1
        WHERE user_id = %s AND cuisine = %s
    '''

    try:
        cursor = connection.cursor()
        cursor.execute(query, (user_id, cuisine))
        connection.commit()
        cursor.close()
            
    except Exception as e:
        print(f"increment_acceptance has an error: {e}")