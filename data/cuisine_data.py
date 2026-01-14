import sqlite3


#Creating Table
def create_cuisine_table(connection):
    query = f'''
        CREATE TABLE IF NOT EXISTS cuisines(
            id INTEGER PRIMARY KEY,
            cuisine TEXT,
            shown INTEGER,
            accepted INTEGER

        )
    '''
    try:
        with connection:
            connection.execute(query)
    except Exception as e:
        print(f"Error: {e}")


#Add row to table
def insert_cuisine(connection, cuisine, shown, accepted):
    query = '''INSERT INTO cuisines (cuisine, shown, accepted) VALUES (?,?,?)'''

    try:
        with connection:
            connection.execute(query, (cuisine, shown, accepted))
    except Exception as e:
        print(f"Error: {e}")


def insert_cuisines(connection, cuisine_list):
    query = "INSERT INTO cuisines (cuisine, shown, accepted) VALUES (?,?,?)"

    try:
        with connection:
            connection.executemany(query, cuisine_list)

    except Exception as e:
        print(f"Error: {e}")


#Query through all rows
def fetch_all_cuisine(connection):
    query = "SELECT * FROM cuisines"

    try:
        with connection:
            rows = connection.execute(query).fetchall()
            return rows
    except Exception as e:
        print(f"Error: {e}")


#Query for specific cuisine
def fetch_cuisine(connection, cuisine):
    query = "SELECT * FROM cuisines WHERE cuisine = ?"

    try:
        with connection:
            return connection.execute(query, (cuisine,)).fetchall()
    except Exception as e:
        print(f"Error: {e}")


#Delete row
def delete_cuisine(connection, id):
    query = "DELETE FROM cuisines WHERE id = ?"

    try:
        with connection:
            connection.execute(query, (id,))
    except Exception as e:
        print(f"Error: {e}")


#Upadating information
def update(connection, cuisine, shown, accept):
    query = "UPDATE cuisines SET shown = shown + ?, accept = accept + ? WHERE cuisine = ?"

    try:
        with connection:
            connection.execute(query, (shown, accept, cuisine))
    except Exception as e:
        print(f"Error: {e}")