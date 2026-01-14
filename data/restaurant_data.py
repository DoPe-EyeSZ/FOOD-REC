import sqlite3


#Creating Table
def create_restaurant_table(connection):
    query = '''
        CREATE TABLE IF NOT EXISTS restaurants(
            place_id TEXT PRIMARY KEY,
            dine_in INTEGER CHECK (dine_in IN (0, 1)),
            take_out INTEGER CHECK (take_out IN (0, 1)),
            vegan_option INTEGER CHECK (vegan_option IN (0, 1)),
            price_level INTEGER CHECK (price_level >=0 AND price_level<=5),
            name TEXT
        )
    '''
    try:
        with connection:
            connection.execute(query)
            connection.commit()

    except Exception as e:
        print(f"create_restaurant_table has an error: {e}")


#Add restaurnt
def insert_restaurant(connection, place_id, dine, togo, vegan, price, name):
    query = '''
        INSERT INTO restaurants (place_id, dine_in, take_out, vegan_option, price_level, name)
        VALUES (?, ?, ?, ?, ?, ?)
    '''

    try:
        with connection:
            connection.execute(query, (place_id, dine, togo, vegan, price, name,))
            connection.commit()
    
    except Exception as e:
        print(f"insert_restaurant has an error: {e}")


#Delete a restaurant
def delete_restaurant(connection, place_id):
    query = '''
        DELETE FROM restaurants WHERE place_id = ?
    '''

    try:
        with connection:
            connection.execute(query, (place_id,))
            connection.commit()

    except Exception as e:
        print(f"delete_restaurant has an error: {e}")


def delete_restaurants(connection):
    query = '''
        DELETE FROM restaurants
    '''

    try:
        with connection:
            connection.execute(query)
            connection.commit()

    except Exception as e:
        print(f"delete_restaurant has an error: {e}")


#Retrieving restaurant
def fetch_restaurant(connection, place_id):
    query = '''
        SELECT FROM restaurants WHERE place_id = ?
    '''

    try:
        with connection:
            return connection.execute(query, (place_id))
        
    except Exception as e:
        print(f"fetch_restaurant has an error: {e}")


def fetch_restaurants(connection):
    query = '''
        SELECT * FROM restaurants
    '''

    try:
        with connection:
            return connection.execute(query).fetchall()
        
    except Exception as e:
        print(f"fetch_restaurants has an error: {e}")