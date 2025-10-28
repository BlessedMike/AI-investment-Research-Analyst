"""
Configuration file for the AI Investment Research Analyst
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# NeMo API Configuration
NEMO_API_URL = os.getenv("NEMO_API_URL", "https://api.nvidia.com/v1/nemo")
NEMO_API_KEY = os.getenv("NEMO_API_KEY", "")

# API Configuration
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1000"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# Cache Configuration
CACHE_TTL = int(os.getenv("CACHE_TTL", "10"))
CACHE_MAX_SIZE = int(os.getenv("CACHE_MAX_SIZE", "100"))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Validation
def validate_config():
    """Validate that required configuration is present"""
    if not NEMO_API_KEY:
        print("⚠️  WARNING: NEMO_API_KEY not set. NeMo analysis endpoints will not work.")
        print("   Set NEMO_API_KEY in your environment or .env file")
        return False
    return True

if __name__ == "__main__":
    validate_config()
