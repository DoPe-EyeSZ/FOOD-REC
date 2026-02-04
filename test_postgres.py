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


    query4 = '''
        SELECT * FROM interactions
    '''

    for place in lite_interaction:
        userid = place[1]
        placeid = place[2]
        rating = place[3]
        rating_count = place[4]
        open = place[5]
        drive = place[6]
        accept = place[7]

        interact_data.insert_user_interaction(pg_connection, placeid, rating, rating_count, open, drive, accept, "test_user")


    cursor = pg_connection.cursor()
    pg_connection.commit()
    cursor.close()

        
        


    print(f"{'='*30} SQLITE {'='*30} ")
    print(len(lite_cuisines))
    print(len(lite_restaurants))
    print(len(lite_interaction))

    
    print(f"{'='*30} POSTGRES {'='*30} ")
    user_count = None
    restaurant_count = restaurant_data.fetch_restaurants(pg_connection)
    cuisine_count = cuisine_data.fetch_all_cuisine(pg_connection)
    interact_count = interact_data.fetch_user_interactions(pg_connection)

    
    print(len(cuisine_count))
    print(len(restaurant_count))
    print(len(interact_count))




    
    
    pg_connection.close()

except Exception as e:
    print(f"error: {e}")