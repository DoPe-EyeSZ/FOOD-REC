from data import data_functions, cuisine_data, interact_data, restaurant_data, user_data

try:
    connection = data_functions.get_connection("test")

    user_data.create_user_table(connection)
    restaurant_data.create_restaurant_table(connection)
    cuisine_data.create_cuisine_table(connection)
    interact_data.create_interact_table(connection)
    connection.commit()
    

    restaurant_data.insert_restaurant(connection, "place_id1", 1, 1, 1, 3, "chinese", "test1")
    restaurant_data.insert_restaurant(connection, "place_id2", 1, 1, 1, 3, "chinese", "test1")

    '''interact_data.insert_user_interaction(connection, "place_id1", 5, 55, 1, 60, 0, "test_user")
    interact_data.insert_user_interaction(connection, "place_id1", 6, 85, 0, 465, 1, "test_user")
    interact_data.insert_user_interaction(connection, "place_id2", 3.3, 55, 1, 60, 0, "test_user")'''
    print(len(interact_data.fetch_user_interactions(connection, user_id="test_user")))
    interact_data.delete_user_interactions(connection, user_id="test_user")
    print(len(interact_data.fetch_user_interactions(connection, user_id="test_user")))
    

    
    
    connection.close()

except Exception as e:
    print(f"error: {e}")