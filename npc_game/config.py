"""
Configuration for the AI NPC Game System
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Groq API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is required. Set it using: export GROQ_API_KEY='your-key-here'")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_TEMPERATURE = float(os.getenv("GROQ_TEMPERATURE", "0.3"))

# Memory Configuration
SHORT_TERM_MEMORY_LIMIT = int(os.getenv("SHORT_TERM_MEMORY_LIMIT", "5"))  # Last N interactions
LONG_TERM_MEMORY_LIMIT = int(os.getenv("LONG_TERM_MEMORY_LIMIT", "50"))  # Total stored interactions

# Emotion Configuration
EMOTIONS = ["neutral", "happy", "sad", "angry", "curious", "afraid", "excited", "disgusted"]
EMOTION_DECAY_RATE = float(os.getenv("EMOTION_DECAY_RATE", "0.1"))  # How fast emotions return to neutral

# Game Configuration
MAX_TURN_LENGTH = int(os.getenv("MAX_TURN_LENGTH", "500"))  # Max characters per player input
