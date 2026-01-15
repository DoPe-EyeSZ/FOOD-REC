import sqlite3

#FOREIGN KEY (user_id) REFERENCES users(user_id),
#Creating Table
def create_cuisine_table(connection):
    query = f'''
        CREATE TABLE IF NOT EXISTS cuisines(
            user_id TEXT DEFAULT 'test_user',
            cuisine TEXT,
            shown INTEGER DEFAULT 0,
            accepted INTEGER DEFAULT 0,
            
            PRIMARY KEY (user_id, cuisine)

        )
    '''
    try:
        with connection:
            connection.execute(query)
    except Exception as e:
        print(f"create_table has an error: {e}")


#Add row to table
def insert_cuisine(connection, cuisine, shown, accepted, user_id = 'test_user'):
    query = '''INSERT INTO cuisines (user_id, cuisine, shown, accepted) VALUES (?,?,?,?)'''

    try:
        with connection:
            connection.execute(query, (user_id, cuisine, shown, accepted))
    except Exception as e:
        print(f"insert_cuisine has an error: {e}")


def insert_cuisines(connection, cuisine_list, user_id = 'test_user'):
    query = "INSERT INTO cuisines (user_id, cuisine, shown, accepted) VALUES (?,?,?,?)"

    try:
        with connection:
            connection.executemany(query, cuisine_list, user_id)

    except Exception as e:
        print(f"insert_cuisines has an error: {e}")


#Query through all rows
def fetch_all_cuisine(connection, user_id = 'test_user'):
    query = "SELECT * FROM cuisines WHERE user_id = ?"

    try:
        with connection:
            rows = connection.execute(query, (user_id,)).fetchall()
            return rows
    except Exception as e:
        print(f"fetch_all_cuisine has an error: {e}")


#Query for specific cuisine
def fetch_cuisine(connection, cuisine, user_id = "test_user"):
    query = "SELECT * FROM cuisines WHERE user_id = ? AND cuisine = ?"

    try:
        with connection:
            return connection.execute(query, (user_id, cuisine,)).fetchall()
    except Exception as e:
        print(f"fetch_cuisine has an error: {e}")


#Delete row
def delete_cuisine(connection, cuisine, user_id = 'test_user'):
    query = "DELETE FROM cuisines WHERE user_id = ? AND cuisine = ?"

    try:
        with connection:
            connection.execute(query, (user_id, cuisine))
    except Exception as e:
        print(f"delete_cuisine has an error: {e}")


def delete_cuisines(connection, user_id = 'test_user'):
    query = "DELETE FROM cuisines WHERE user_id = ?"

    try:
        with connection:
            connection.execute(query, (user_id,))

    except Exception as e:
        print(f"delete_cuisines has an error: {e}")


#Upadating information
def update_cuisine_stats(connection, cuisine, accepted, user_id = 'test_user'):
    query = '''
        INSERT INTO cuisines (user_id, cuisine, shown, accepted)
        VALUES (?, ?, 1, ?)
        ON CONFLICT(user_id, cuisine)
        DO UPDATE SET
            shown = shown + 1,
            accepted = accepted + ?
    '''

    try:
        with connection:
            connection.execute(query, (user_id, cuisine, accepted, accepted))
    except Exception as e:
        print(f"update_cuisine_stats has an error: {e}")