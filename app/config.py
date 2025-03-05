import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")


config = Config()
