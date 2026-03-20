import os
from dotenv import load_dotenv

load_dotenv(".env.bot.secret")

LMS_API_URL = os.getenv("LMS_API_URL")
LMS_API_KEY = os.getenv("LMS_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
