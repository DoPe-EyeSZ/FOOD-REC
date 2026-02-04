
#Creating Table
def create_cuisine_table(connection):
    query = f'''
        CREATE TABLE IF NOT EXISTS cuisine_stats(
            username TEXT DEFAULT 'test_user',
            cuisine TEXT,
            shown INTEGER DEFAULT 0,
            accepted INTEGER DEFAULT 0,
            PRIMARY KEY (username, cuisine),
            FOREIGN KEY (username) REFERENCES users(username)

        )
    '''
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()

    except Exception as e:
        print(f"create_cuisine_table has an error: {e}")


#Query through all rows
def fetch_all_cuisine(connection, username = 'test_user'):
    query = "SELECT * FROM cuisine_stats WHERE username = %s"

    try:
        cursor = connection.cursor()
        cursor.execute(query, (username,))
        rows = cursor.fetchall()
        cursor.close()
        return rows
        
    except Exception as e:
        print(f"fetch_all_cuisine has an error: {e}")


#Query for specific cuisine
def fetch_cuisine(connection, cuisine, username = "test_user"):
    query = "SELECT * FROM cuisine_stats WHERE username = %s AND cuisine = %s"

    try:
            
        cursor = connection.cursor()
        cursor.execute(query, (username, cuisine,))
        row = cursor.fetchone()
        cursor.close()

        return row
    
    except Exception as e:
        print(f"fetch_cuisine has an error: {e}")


#Delete row
def delete_cuisine(connection, cuisine, username = 'test_user'):
    query = "DELETE FROM cuisine_stats WHERE username = %s AND cuisine = %s"

    try:
        cursor = connection.cursor()
        cursor.execute(query, (username, cuisine,))
        connection.commit()
        cursor.close()
        print('success')
            
    except Exception as e:
        print(f"delete_cuisine has an error: {e}")



#Upsert cuisine information
def upsert_cuisine_stats(connection, cuisine, accepted, username = 'test_user'):
    query = '''
        INSERT INTO cuisine_stats (username, cuisine, shown, accepted)
        VALUES (%s, %s, 1, %s)
        ON CONFLICT(username, cuisine)
        DO UPDATE SET
            shown = cuisine_stats.shown + 1,
            accepted = cuisine_stats.accepted + %s
    '''

    try:
        cursor = connection.cursor()
        cursor.execute(query, (username, cuisine, accepted, accepted))
        connection.commit()
        cursor.close()

    except Exception as e:
        print(f"upsert_cuisine_stats has an error: {e}")


def increment_acceptance(connection, cuisine, username = 'test_user'):
    query = '''
        UPDATE cuisine_stats
        SET accepted = accepted + 1
        WHERE username = %s AND cuisine = %s
    '''

    try:
        cursor = connection.cursor()
        cursor.execute(query, (username, cuisine))
        connection.commit()
        cursor.close()
            
    except Exception as e:
        print(f"increment_acceptance has an error: {e}")