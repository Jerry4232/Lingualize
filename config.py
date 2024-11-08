# config.py
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Access API keys
OpenAI_API_KEY = os.getenv("GPT_API_KEY")
ASSEMBLY_API_KEY = os.getenv("ASSEMBLY_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
XI_API_KEY = os.getenv("XI_API_KEY")
