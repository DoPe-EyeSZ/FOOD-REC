from data import data_functions, cuisine_data, interact_data, restaurant_data, user_data
import sqlite3
from api import api_function
from werkzeug.security import generate_password_hash, check_password_hash

try:
    test_connection = data_functions.get_connection("test")
    prod_connection = data_functions.get_connection("prod")

    user_data.create_user_table(test_connection)
    test_connection.commit()



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

    
    print(f"{'='*30} POSTGRES TEST {'='*30} ")
    user_count = None
    restaurant = restaurant_data.fetch_restaurants(test_connection)
    cuisine = cuisine_data.fetch_all_cuisine(test_connection, user_id=1)
    interact = interact_data.fetch_user_interactions(test_connection, user_id= 1)

    restaurant2 = restaurant_data.fetch_restaurants(prod_connection)
    cuisine2 = cuisine_data.fetch_all_cuisine(prod_connection, user_id=1)
    interact2 = interact_data.fetch_user_interactions(prod_connection, user_id= 1)

    
    print(len(cuisine))
    print(len(restaurant))
    print(len(interact))

    print(f"{'='*30} POSTGRES PROD {'='*30} ")

    print(len(cuisine2))
    print(len(restaurant2))
    print(len(interact2))

    pw = "test_pw_hash"
    all_cuisines = cuisine_data.fetch_all_cuisine(prod_connection, 1)
    all_interactions = interact_data.fetch_user_interactions(prod_connection, 1)

    highest_appearance = []
    highest_acceptance = []

    for info in all_cuisines:
        cuisine = info[1]
        appear = info[2]
        accept = info[3]
        
        if appear > 3:
            highest_acceptance.append([cuisine, round(accept/appear, 2)])
        highest_appearance.append(list(info[1:]))

    highest_appearance.sort(key = lambda c: c[1], reverse=True)
    highest_acceptance.sort(key = lambda c:c[1], reverse=True)

    print(highest_appearance[:10])       #Cuisine user seen the most
    print(highest_acceptance[:10])       #Cuisine program thinks user like the most
    print(len(all_cuisines))        #Number of cuisines users have seen
    print(len(all_interactions))        #Number of restaurants interacted with



    









    
    
    test_connection.close()
    prod_connection.close()

except Exception as e:
    print(f"error: {e}")