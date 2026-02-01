from data import data_functions, cuisine_data, interact_data, restaurant_data, user_data

try:
    connection = data_functions.get_connection("test")

    
    
    user_data.create_user_table(connection)


    #restaurant_data.create_restaurant_table(connection)
    #cuisine_data.create_cuisine_table(connection)
    #interact_data.create_interact_table(connection)
    
    
    print("finished")



    connection.close()

except Exception as e:
    print(f"error: {e}")