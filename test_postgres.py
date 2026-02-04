from data import data_functions, cuisine_data, interact_data, restaurant_data, user_data
import sqlite3

try:
    pg_connection = data_functions.get_connection("test")
    lite_connection = sqlite3.connect("instance/test_data.db")

    query1 = '''
        SELECT * FROM interactions
    '''
    lite_interaction = lite_connection.execute(query1).fetchall()


    query2 = '''
        SELECT * from restaurants
    '''
    lite_restaurants = lite_connection.execute(query2).fetchall()


    query3 = '''
        SELECT * FROM cuisines
    '''
    lite_cuisines = lite_connection.execute(query3).fetchall()


    print(len(lite_cuisines))
    print(len(lite_restaurants))
    print(lite_interaction)


    user_data.create_user_table(pg_connection)
    restaurant_data.create_restaurant_table(pg_connection)
    cuisine_data.create_cuisine_table(pg_connection)
    interact_data.create_interact_table(pg_connection)
    pg_connection.commit()
    

    

    user_count = None
    restaurant_count = restaurant_data.fetch_restaurants(pg_connection)
    cuisine_count = cuisine_data.fetch_all_cuisine(pg_connection)
    interact_count = interact_data.fetch_user_interactions(pg_connection)

    print(len(restaurant_count))
    print(len(cuisine_count))
    print(len(interact_count))




    
    
    pg_connection.close()

except Exception as e:
    print(f"error: {e}")