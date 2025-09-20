import os
from dotenv import load_dotenv
import warnings

# --- Environment Variable Loading ---
# This section loads API keys and configuration settings from a .env file.
# This keeps sensitive information separate from the code.
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")
GEMINI_LLM_MODEL = os.getenv("GEMINI_LLM_MODEL")
LOL_LOCKFILE_PATH = os.getenv("LOL_LOCKFILE_PATH")

# Suppress warnings, useful for self-signed SSL certificates.
warnings.filterwarnings("ignore")