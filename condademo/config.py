from dotenv import load_dotenv
import os 

load_dotenv()

mongo_uri = os.environ.get("MONGO_URI")
data_col = os.environ.get("DATA_COLLECTION")