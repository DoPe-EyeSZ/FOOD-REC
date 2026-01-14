import sqlite3

def get_connection(db_name):
    try:
        path = "instance/" + db_name
        return sqlite3.connect(path)
    except Exception as e:
        print(f"Error: {e}")


#Creating Table
def create_cuisine_table(connection):
    query = f'''
        CREATE TABLE IF NOT EXISTS cuisine(
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
    query = '''INSERT INTO cuisine (cuisine, shown, accepted) VALUES (?,?,?)'''

    try:
        with connection:
            connection.execute(query, (cuisine, shown, accepted))
    except Exception as e:
        print(f"Error: {e}")


#Query through all rows
def fetch_all_cuisine(connection):
    query = "SELECT * FROM cuisine"

    try:
        with connection:
            rows = connection.execute(query).fetchall()
            return rows
    except Exception as e:
        print(f"Error: {e}")


#Query for specific cuisine
def fetch_cuisine(connection, cuisine):
    query = "SELECT * FROM cuisine WHERE cuisine = ?"

    try:
        with connection:
            return connection.execute(query, (cuisine,)).fetchall()
    except Exception as e:
        print(f"Error: {e}")



#Delete row
def delete_cuisine(connection, id):
    query = "DELETE FROM cuisine WHERE id = ?"

    try:
        with connection:
            connection.execute(query, (id))
    except Exception as e:
        print(f"Error: {e}")