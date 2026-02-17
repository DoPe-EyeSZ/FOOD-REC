
#Creating table
def create_user_table(connection):
    query = '''
        CREATE TABLE IF NOT EXISTS users(
            user_id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    '''

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()

    except Exception as e:
        print(f"create_user_table has an error: {e}")

def fetch_user_credentials(connection, username):
    query = '''
        SELECT user_id, password_hash FROM users WHERE username = %s
    '''

    try:
        cur = connection.cursor()
        cur.execute(query, (username,))
        data = cur.fetchone()
        cur.close()
        return data
    
    except Exception as e:
        print(f"fetch_all_user_id has an error: {e}")


def fetch_user_id_credentials(connection, user_id):
    query = '''
        SELECT username, password_hash FROM users WHERE user_id = %s
    '''

    try:
        cur = connection.cursor()
        cur.execute(query, (user_id,))
        data = cur.fetchone()
        cur.close()
        return data
    
    except Exception as e:
        print(f"fetch_all_user_id has an error: {e}")

def create_user(connection, username, password_hash):
    query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"

    try:
        cur = connection.cursor()
        cur.execute(query, (username, password_hash,))
        connection.commit()
        cur.close()
    
    except Exception as e:
        print(f"create_user has an error: {e}")

def update_username(connection, new_username, user_id):
    query = "UPDATE users SET username = %s WHERE user_id = %s"

    try:
        cur = connection.cursor()
        cur.execute(query, (new_username, user_id))
        connection.commit()
        cur.close()
    
    except Exception as e:
        print(f"update_username has an error: {e}")


def change_pw(connection, new_pw_hash, user_id):
    query = "UPDATE users SET password_hash = %s WHERE user_id = %s"

    try:
        cur = connection.cursor()
        cur.execute(query, (new_pw_hash, user_id))
        connection.commit()
        cur.close()
    
    except Exception as e:
        print(f"change_pw has an error: {e}")


def delete_user(connection, user_id):
    query = "DELETE FROM users WHERE user_id = %s"

    try:
        cur = connection.cursor()
        cur.execute(query, (user_id,))
        connection.commit()
        cur.close()

    except Exception as e:
        print(f"delete_user has an error: {e}")