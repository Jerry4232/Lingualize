# config.py
"""
This module loads and provides access to API keys and other configuration variables
from environment variables, specifically from a `.env` file. By using the `dotenv` package,
it reads sensitive information, such as API keys, in a secure manner without hard-coding
these values into the code.
"""

import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Access API keys
OpenAI_API_KEY = os.getenv("GPT_API_KEY")
ASSEMBLY_API_KEY = os.getenv("ASSEMBLY_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
XI_API_KEY = os.getenv("XI_API_KEY")
