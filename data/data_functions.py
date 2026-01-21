import sqlite3

def get_connection(db_name):
    try:
        path = "instance/" + db_name
        return sqlite3.connect(path)
    except Exception as e:
        print(f"Error: {e}")

def join_interaction_restaurant(connection, user_id = "test_user"):
    query = '''
        SELECT r.dine_in, r.take_out, r.vegan_option, r.price_level, r.cuisine,
        i.rating, i.rating_count, i.is_open, i.drive_time, i.accepted
        FROM restaurants r
        JOIN interactions i
        ON r.place_id = i.place_id
        WHERE i.user_id = ?
    '''

    try:
        with connection:
            return connection.execute(query, (user_id,)).fetchall()

    except Exception as e:
        print(f"join_interaction_restaurant has an error: {e}")