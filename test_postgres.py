from data import data_functions

try:
    connection = data_functions.get_connection(db_type="prod")
    print("data success")

    connection2 = data_functions.get_connection("test")
    print("test success")
    connection.close()

except Exception as e:
    print(f"error: {e}")