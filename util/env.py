import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
MY_GUILD_ID = os.getenv("MY_GUILD_ID")
VOICEVOX_BASE_URL= os.getenv("VOICEVOX_BASE_URL")
