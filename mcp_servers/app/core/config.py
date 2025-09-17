import os
from dotenv import load_dotenv

load_dotenv()

API_V1_BASE_ROUTE=os.getenv('API_V1_BASE_ROUTE')
TOOLS_FILE=os.getenv('TOOLS_FILE')
PROVIDERS_FILE=os.getenv("PROVIDERS_FILE")
