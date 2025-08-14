import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///splitwise_bot.db')
    
    @classmethod
    def validate(cls):
        if not cls.DISCORD_TOKEN:
            raise ValueError("DISCORD_TOKEN environment variable is required")
        return True