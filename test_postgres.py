from data import data_functions

try:
    connection = data_functions.get_connection(db_type="prod")

    connection2 = data_functions.get_connection("test")
    connection.close()

except Exception as e:
    print(f"error: {e}")