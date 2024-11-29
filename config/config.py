import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
XAI_API_KEY = os.getenv("XAI_API_KEY")

if not XAI_API_KEY:
    logger.warning("XAI_API_KEY not found in environment variables. Please set it in your .env file.")

# Environment configuration
ENV = os.getenv("FLASK_ENV", "development")
DEBUG = ENV == "development"
