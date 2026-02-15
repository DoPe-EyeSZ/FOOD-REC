import pickle

def create_user_models_table(connection):
    query = '''
        CREATE TABLE IF NOT EXISTS user_models(
            user_id INTEGER PRIMARY KEY,
            model_data BYTEA,
            scaler_data BYTEA,
            cv_mean FLOAT,
            interaction_count INTEGER,
            trained_at TIMESTAMP DEFAULT NOW(),
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
    '''
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        print("user_models table created")
    
    except Exception as e:
        print(f"create_user_models_table has an error: {e}")


def save_user_model(connection, user_id, model, scaler, cv_mean, interaction_count):
    
    # Convert model and scaler to binary
    model_bytes = pickle.dumps(model)
    scaler_bytes = pickle.dumps(scaler)
    
    query = '''
        INSERT INTO user_models (user_id, model_data, scaler_data, cv_mean, interaction_count)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (user_id) 
        DO UPDATE SET
            model_data = EXCLUDED.model_data,
            scaler_data = EXCLUDED.scaler_data,
            cv_mean = EXCLUDED.cv_mean,
            interaction_count = EXCLUDED.interaction_count,
            trained_at = NOW()
    '''
    
    try:
        cursor = connection.cursor()
        cursor.execute(query, (user_id, model_bytes, scaler_bytes, cv_mean, interaction_count))
        connection.commit()
        cursor.close()
        print(f"Model saved for user {user_id}")
    
    except Exception as e:
        print(f"save_user_model has an error: {e}")


def load_user_model(connection, user_id):
    """Load model and scaler from database"""
    
    query = "SELECT model_data, scaler_data FROM user_models WHERE user_id = %s"
    
    try:
        cursor = connection.cursor()
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        cursor.close()
        
        if not result:
            print(f"No model found for user {user_id}")
            return None, None
        
        # Convert binary back to model and scaler
        model = pickle.loads(result[0])
        scaler = pickle.loads(result[1])
        
        print(f"Model loaded for user {user_id}")
        return model, scaler
    
    except Exception as e:
        print(f"load_user_model has an error: {e}")
        return None, None
    


def delete_user_model(connection, user_id):
    """Delete user's model from database"""
    query = "DELETE FROM user_models WHERE user_id = %s"
    
    try:
        cursor = connection.cursor()
        cursor.execute(query, (user_id,))
        connection.commit()
        cursor.close()
        print(f"Model deleted for user {user_id}")
    
    except Exception as e:
        print(f"delete_user_model has an error: {e}")


def fetch_model_data(connection, user_id):
    query = "SELECT * FROM user_models WHERE user_id = %s"

    try:
        cur = connection.cursor()
        cur.execute(query, (user_id,))
        data = cur.fetchone()
        cur.close()

        return data

    except Exception as e:
        print(f"fetch_model_data has an error: {e}")