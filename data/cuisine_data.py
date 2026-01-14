import sqlite3


#Creating Table
def create_cuisine_table(connection):
    query = f'''
        CREATE TABLE IF NOT EXISTS cuisines(
            cuisine TEXT PRIMARY KEY,
            shown INTEGER DEFAULT 0,
            accepted INTEGER DEFAULT 0

        )
    '''
    try:
        with connection:
            connection.execute(query)
    except Exception as e:
        print(f"create_table has an error: {e}")


#Add row to table
def insert_cuisine(connection, cuisine, shown, accepted):
    query = '''INSERT INTO cuisines (cuisine, shown, accepted) VALUES (?,?,?)'''

    try:
        with connection:
            connection.execute(query, (cuisine, shown, accepted))
            connection.commit()
    except Exception as e:
        print(f"insert_cuisine has an error: {e}")


def insert_cuisines(connection, cuisine_list):
    query = "INSERT INTO cuisines (cuisine, shown, accepted) VALUES (?,?,?)"

    try:
        with connection:
            connection.executemany(query, cuisine_list)
            connection.commit()

    except Exception as e:
        print(f"insert_cuisines has an error: {e}")


#Query through all rows
def fetch_all_cuisine(connection):
    query = "SELECT * FROM cuisines"

    try:
        with connection:
            rows = connection.execute(query).fetchall()
            return rows
    except Exception as e:
        print(f"fetch_all_cuisine has an error: {e}")


#Query for specific cuisine
def fetch_cuisine(connection, cuisine):
    query = "SELECT * FROM cuisines WHERE cuisine = ?"

    try:
        with connection:
            return connection.execute(query, (cuisine,)).fetchall()
    except Exception as e:
        print(f"fetch_cuisine has an error: {e}")


#Delete row
def delete_cuisine(connection, id):
    query = "DELETE FROM cuisines WHERE id = ?"

    try:
        with connection:
            connection.execute(query, (id,))
            connection.commit()
    except Exception as e:
        print(f"delete_cuisine has an error: {e}")


def delete_cuisines(connection):
    query = "DELETE FROM cuisines"

    try:
        with connection:
            connection.execute(query)
            connection.commit()

    except Exception as e:
        print(f"delete_cuisines has an error: {e}")


#Upadating information
def update_cuisine_stats(connection, cuisine, accepted):
    query = '''
        INSERT INTO cuisines (cuisine, shown, accepted)
        VALUES (?, 1, ?)
        ON CONFLICT(cuisine)
        DO UPDATE SET
            shown = shown + 1,
            accepted = accepted + ?
    '''

    try:
        with connection:
            connection.execute(query, (cuisine, accepted, accepted))
            connection.commit()
    except Exception as e:
        print(f"update_cuisine_stats has an error: {e}")