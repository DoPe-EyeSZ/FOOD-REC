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




    information1 = cuisine_data.fetch_all_cuisine(prod_connection, 1)
    information2 = interact_data.fetch_user_interactions(prod_connection, 1)
    print(len(information2))

    new = []
    for info in information1:
        new.append(list(info[1:]))

    highest_appearance = sorted(new, key=lambda n: n[1], reverse=True )
    print(highest_appearance )
    print()

    new2 = []

    for info in information1:
        acceptance = info[3]/info[2]
        new2.append([info[1], round(acceptance, 2)])

    highest_acceptance = sorted(new2, reverse=True, key=lambda n: n[1])

    print(highest_acceptance)







    
    
    test_connection.close()
    prod_connection.close()

except Exception as e:
    print(f"error: {e}")