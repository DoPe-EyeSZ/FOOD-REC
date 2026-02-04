from data import data_functions, cuisine_data, interact_data, restaurant_data, user_data

try:
    connection = data_functions.get_connection("test")

    user_data.create_user_table(connection)
    restaurant_data.create_restaurant_table(connection)
    cuisine_data.create_cuisine_table(connection)
    interact_data.create_interact_table(connection)
    connection.commit()
    

    # restaurants
    restaurant_data.insert_restaurant(connection, "place_id1", 0, 0, 0, 5, "chinese", "test1") 
    restaurant_data.insert_restaurant(connection, "place_id2", 1, 0, 1, 3, "chinese", "test1")
    restaurant_data.insert_restaurant(connection, "place_id3", 1, 1, 0, 4, "japanese", "test2")
    restaurant_data.insert_restaurant(connection, "place_id4", 0, 1, 1, 2, "mexican", "test3")
    restaurant_data.insert_restaurant(connection, "place_id5", 1, 0, 0, 5, "italian", "test4")
    restaurant_data.insert_restaurant(connection, "place_id6", 0, 0, 1, 3, "thai", "test5")
    restaurant_data.insert_restaurant(connection, "place_id7", 1, 1, 1, 4, "american", "test6")
    restaurant_data.insert_restaurant(connection, "place_id8", 0, 1, 0, 1, "korean", "test7")
    restaurant_data.insert_restaurant(connection, "place_id9", 1, 0, 1, 2, "indian", "test8")
    restaurant_data.insert_restaurant(connection, "place_id10", 0, 0, 0, 5, "vietnamese", "test9")

    # interactions
    '''interact_data.insert_user_interaction(connection, "place_id1", 4.0, 1200, 1, 200, 0, "test_user")
    interact_data.insert_user_interaction(connection, "place_id2", 2.5, 800, 0, 150, 1, "test_user")
    interact_data.insert_user_interaction(connection, "place_id3", 5.0, 3000, 1, 500, 1, "test_user")
    interact_data.insert_user_interaction(connection, "place_id4", 1.5, 400, 0, 50, 0, "test_user")
    interact_data.insert_user_interaction(connection, "place_id5", 4.5, 2200, 1, 320, 1, "test_user")
    interact_data.insert_user_interaction(connection, "place_id6", 3.0, 1400, 0, 210, 0, "test_user")
    interact_data.insert_user_interaction(connection, "place_id7", 4.2, 2600, 1, 410, 1, "test_user")
    interact_data.insert_user_interaction(connection, "place_id8", 2.0, 600, 0, 90, 0, "test_user")
    interact_data.insert_user_interaction(connection, "place_id9", 3.8, 1750, 1, 275, 1, "test_user")
    interact_data.insert_user_interaction(connection, "place_id10", 4.7, 3100, 1, 520, 1, "test_user")

    interact_data.insert_user_interaction(connection, "place_id1", 3.2, 900, 0, 130, 0, "test_user")
    interact_data.insert_user_interaction(connection, "place_id2", 4.1, 2000, 1, 340, 1, "test_user")
    interact_data.insert_user_interaction(connection, "place_id3", 2.8, 700, 0, 95, 0, "test_user")
    interact_data.insert_user_interaction(connection, "place_id4", 3.6, 1500, 1, 240, 1, "test_user")
    interact_data.insert_user_interaction(connection, "place_id5", 4.9, 3300, 1, 600, 1, "test_user")
    interact_data.insert_user_interaction(connection, "place_id6", 1.9, 450, 0, 60, 0, "test_user")
    interact_data.insert_user_interaction(connection, "place_id7", 3.7, 1600, 1, 250, 0, "test_user")
    interact_data.insert_user_interaction(connection, "place_id8", 2.3, 650, 0, 85, 0, "test_user")
    interact_data.insert_user_interaction(connection, "place_id9", 4.4, 2400, 1, 380, 1, "test_user")
    interact_data.insert_user_interaction(connection, "place_id10", 3.1, 1100, 0, 170, 0, "test_user")'''
        


    print(len(restaurant_data.fetch_restaurants(connection,)))
    print(len(interact_data.fetch_user_interactions(connection, "test_user")))
    print(data_functions.join_10_restaurant(connection, "test_user"))




    
    
    connection.close()

except Exception as e:
    print(f"error: {e}")