
#Creating Table
def create_restaurant_table(connection):
    query = '''
        CREATE TABLE IF NOT EXISTS restaurants(
            place_id TEXT PRIMARY KEY,
            dine_in INTEGER CHECK (dine_in IN (0, 1)),
            take_out INTEGER CHECK (take_out IN (0, 1)),
            vegan_option INTEGER CHECK (vegan_option IN (0, 1)),
            price_level INTEGER CHECK (price_level >=0 AND price_level<=5),
            cuisine TEXT, 
            name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    '''
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()

    except Exception as e:
        print(f"create_restaurant_table has an error: {e}")


#Add restaurnt
def insert_restaurant(connection, place_id, dine, togo, vegan, price, cuisine, name):
    query = '''
        INSERT INTO restaurants (place_id, dine_in, take_out, vegan_option, price_level, cuisine, name)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT(place_id)
        DO UPDATE SET
            dine_in = excluded.dine_in,
            take_out = excluded.take_out,
            vegan_option = excluded.vegan_option,
            price_level = excluded.price_level,
            cuisine = excluded.cuisine,
            name = excluded.name
        WHERE
            dine_in <> excluded.dine_in
            OR take_out <> excluded.take_out
            OR vegan_option <> excluded.vegan_option
            OR price_level <> excluded.price_level
            OR cuisine <> excluded.cuisine
            OR name <> excluded.name;
    '''

    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, (place_id, dine, togo, vegan, price, cuisine, name,))
            connection.commit()
            cursor.close()
    
    except Exception as e:
        print(f"insert_restaurant has an error: {e}")


#Delete a restaurant
def delete_restaurant(connection, place_id):
    query = '''
        DELETE FROM restaurants WHERE place_id = %s
    '''

    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, (place_id,))
            connection.commit()
            cursor.close()

    except Exception as e:
        print(f"delete_restaurant has an error: {e}")


def delete_restaurants(connection):
    query = '''
        DELETE FROM restaurants
    '''

    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()

    except Exception as e:
        print(f"delete_restaurant has an error: {e}")


#Retrieving restaurant
def fetch_restaurant(connection, place_id):
    query = '''
        SELECT * FROM restaurants WHERE place_id = %s
    '''

    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, (place_id,))
            data = cursor.fetchone()
            cursor.close()
            return data
        
    except Exception as e:
        print(f"fetch_restaurant has an error: {e}")


def fetch_restaurants(connection):
    query = '''
        SELECT * FROM restaurants
    '''

    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
            return data
        
    except Exception as e:
        print(f"fetch_restaurants has an error: {e}")