import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# GitHub
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")

# Vercel
VERCEL_TOKEN = os.getenv("VERCEL_TOKEN")
VERCEL_DEPLOY_HOOK = os.getenv("VERCEL_DEPLOY_HOOK")   # Deploy hook URL
VERCEL_PROJECT_ID = os.getenv("VERCEL_PROJECT_ID")     # Project name/ID

# Render
RENDER_API_KEY = os.getenv("RENDER_API_KEY")
RENDER_DEPLOY_HOOK = os.getenv("RENDER_DEPLOY_HOOK")   # Deploy hook URL
RENDER_SERVICE_ID = os.getenv("RENDER_SERVICE_ID")     # Service ID (srv-xxxx)

# Security — comma-separated Telegram user IDs allowed to use the bot
# Leave empty to allow anyone (not recommended)
ALLOWED_USER_IDS_RAW = os.getenv("ALLOWED_USER_IDS", "")
ALLOWED_USER_IDS = (
    [int(uid.strip()) for uid in ALLOWED_USER_IDS_RAW.split(",") if uid.strip()]
    if ALLOWED_USER_IDS_RAW
    else []
)
