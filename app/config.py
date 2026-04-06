from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY      = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY  = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")
REDIS_URL           = os.getenv("REDIS_URL", "redis://localhost:6379")