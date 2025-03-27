import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
APP_TOKEN = os.getenv("APP_TOKEN")