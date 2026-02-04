from data import data_functions, cuisine_data, interact_data, restaurant_data, user_data

try:
    connection = data_functions.get_connection("test")

    user_data.create_user_table(connection)
    restaurant_data.create_restaurant_table(connection)
    cuisine_data.create_cuisine_table(connection)
    interact_data.create_interact_table(connection)
    connection.commit()
    

    restaurant_data.insert_restaurant(connection, "place_id1", 0, 0, 0, 0, "chinese", "test1")
    restaurant_data.insert_restaurant(connection, "place_id2", 1, 1, 1, 1, "chinese", "test1")
    restaurant_data.insert_restaurant(connection, "place_id3", 1, 0, 1, 0, "chinese", "test1")


    print(len(restaurant_data.fetch_restaurants(connection,)))
    restaurant_data.delete_restaurant(connection, "place_id2")
    print(len(restaurant_data.fetch_restaurants(connection,)))
    restaurant_data.delete_restaurants(connection)
    print(len(restaurant_data.fetch_restaurants(connection,)))




    
    
    connection.close()

except Exception as e:
    print(f"error: {e}")