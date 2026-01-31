from data import data_functions

try:
    connection = data_functions.get_connection(db_type="production")
    print("data success")
    connection.close()

except Exception as e:
    print(f"error: {e}")