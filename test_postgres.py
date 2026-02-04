from data import data_functions, cuisine_data, interact_data, restaurant_data, user_data
import sqlite3
from api import api_function

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


        
        


    print(f"{'='*30} SQLITE {'='*30} ")
    print(len(lite_cuisines))
    print(len(lite_restaurants))
    print(len(lite_interaction))

    
    print(f"{'='*30} POSTGRES {'='*30} ")
    user_count = None
    restaurant = restaurant_data.fetch_restaurants(pg_connection)
    cuisine = cuisine_data.fetch_all_cuisine(pg_connection)
    interact = interact_data.fetch_user_interactions(pg_connection)

    
    print(cuisine)
    print(api_function.find_frequency(pg_connection))
    print(len(restaurant))
    print(len(interact))




    
    
    pg_connection.close()

except Exception as e:
    print(f"error: {e}")