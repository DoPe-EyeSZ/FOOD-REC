
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from data import data_functions
from ML import ml_model

from dotenv import load_dotenv
load_dotenv()


connection = data_functions.get_connection("prod")

data = ml_model.train_save_model(connection, user_id=1, coldstart=False)







connection.close()