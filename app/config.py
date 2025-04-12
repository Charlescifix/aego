# app/config.py
import os
from dotenv import load_dotenv
import logging

load_dotenv()

API_KEY = os.getenv("API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
DATABASE_URL = os.getenv("DATABASE_URL")
AEGO_TOKEN_ADDRESS = os.getenv("AEGO_TOKEN_ADDRESS")
SOL_RPC_URL = os.getenv("SOL_RPC_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger("aegobot")
