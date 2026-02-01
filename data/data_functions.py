import sqlite3
import psycopg2
from config import POSTGRES_HOST, POSTGRES_DB_TEST, POSTGRES_DB_PROD, POSTGRES_USER, POSTGRES_PASSWORD

def get_connection(db_type = "test"):

    if db_type == "test":
        database = POSTGRES_DB_TEST
    else:
        database = POSTGRES_DB_PROD
        
    connection = psycopg2.connect(host = POSTGRES_HOST, 
                                  database = database, 
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
        WHERE i.user_id = %s
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
        WHERE i.user_id = %s
        ORDER BY i.id DESC 
        LIMIT 10
    '''

    try:
        with connection:
            return connection.execute(query, (user_id,)).fetchall()

    except Exception as e:
        print(f"join_interaction_restaurant has an error: {e}")