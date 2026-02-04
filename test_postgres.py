from data import data_functions, cuisine_data, interact_data, restaurant_data, user_data
import sqlite3
from api import api_function

try:
    pg_connection = data_functions.get_connection("test")
    pg_connection2 = data_functions.get_connection("prod")

    '''restaurant_data.create_restaurant_table(pg_connection)
    user_data.create_user_table(pg_connection)
    cuisine_data.create_cuisine_table(pg_connection)
    interact_data.create_interact_table(pg_connection)

    pg_connection.commit()


    lite_connection = sqlite3.connect("instance/test_data.db")

    query1 = "SELECT * FROM interactions"
    lite_interaction = lite_connection.execute(query1).fetchall()


    query2 = "SELECT * from restaurants"
    lite_restaurants = lite_connection.execute(query2).fetchall()


    query3 = "SELECT * FROM cuisines"
    lite_cuisines = lite_connection.execute(query3).fetchall()

    


    print(f"{'='*30} SQLITE {'='*30} ")
    print(len(lite_cuisines))
    print(len(lite_restaurants))
    print(len(lite_interaction))

    
    print(f"{'='*30} POSTGRES {'='*30} ")
    user_count = None
    restaurant = restaurant_data.fetch_restaurants(pg_connection)
    cuisine = cuisine_data.fetch_all_cuisine(pg_connection)
    interact = interact_data.fetch_user_interactions(pg_connection)

    restaurant2 = restaurant_data.fetch_restaurants(pg_connection2)
    cuisine2 = cuisine_data.fetch_all_cuisine(pg_connection2)
    interact2 = interact_data.fetch_user_interactions(pg_connection2)

    
    print(len(cuisine))
    print(len(restaurant))
    print(len(interact))

    print(f"{'='*30} POSTGRES PROD {'='*30} ")

    print(len(cuisine2))
    print(len(restaurant2))
    print(len(interact2))

    '''
    query4 = '''
        ALTER TABLE user_interactions
        ADD CONSTRAINT user_interactions_fkey
        FOREIGN KEY (username) REFERENCES users(username)
    '''


    cur = pg_connection2.cursor()

    cur.execute(query4, )
    pg_connection2.commit()
    cur.close()







    
    
    pg_connection.close()
    pg_connection2.close()

except Exception as e:
    print(f"error: {e}")