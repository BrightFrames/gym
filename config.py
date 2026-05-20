# config.py
import os

class Config:
    """Set Flask configuration variables from environment variables."""

    # Get the secret key from the environment
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Get the database URL from the environment
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Engine options for Supabase/Neon PostgreSQL
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # Gemini API Key
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')