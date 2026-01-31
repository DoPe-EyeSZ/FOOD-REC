import sqlite3
import psycopg2
from config import POSTGRES_HOST, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD

def get_connection(db_name = None, db_type = "dev"):

    if db_type == "dev":
        try:
            path = "instance/" + db_name
            return sqlite3.connect(path)
        except Exception as e:
            print(f"Error: {e}")

    else:
        connection = psycopg2.connect(host = POSTGRES_HOST, 
                                      database = POSTGRES_DB, 
                                      user = POSTGRES_USER, 
                                      password = POSTGRES_PASSWORD)
        return connection


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


def join_10_restaurant(connection, user_id = "test_user"):
    query = '''
        SELECT r. name, r.dine_in, r.take_out, r.vegan_option, r.price_level, r.cuisine,
        i.rating, i.rating_count, i.is_open, i.drive_time, i.accepted
        FROM restaurants r
        JOIN interactions i
        ON r.place_id = i.place_id
        WHERE i.user_id = ?
        ORDER BY i.id DESC 
        LIMIT 10
    '''

    try:
        with connection:
            return connection.execute(query, (user_id,)).fetchall()

    except Exception as e:
        print(f"join_interaction_restaurant has an error: {e}")