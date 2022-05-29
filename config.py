import os

from dotenv import load_dotenv
load_dotenv()

SERVICE_ACCOUNT_JSON = os.getenv("SERVICE_ACCOUNT_JSON")
DATASET = os.getenv("DATASET")