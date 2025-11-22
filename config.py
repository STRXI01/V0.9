import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

API_ID = int(getenv("API_ID", "6435225"))
API_HASH = getenv("API_HASH", "4e984ea35f854762dcde906dce426c2d")
BOT_PRIVACY = getenv("BOT_PRIVACY", "https://telegra.ph/Privacy-Policy-for-Syphix-10-06")
BOT_TOKEN = getenv("BOT_TOKEN", "")

API_URL = getenv("API_URL", "https://space.in")
COOKIE_URL = getenv("COOKIE_URL")

MONGO_DB_URI = getenv("MONGO_DB_URI", "")

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 600))

LOG_GROUP_ID = int(getenv("LOG_GROUP_ID",-1002139499282))

OWNER_ID = int(getenv("OWNER_ID", 8338247560))

OWNER = int(getenv("OWNER", 8338247560))

HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")

HEROKU_API_KEY = getenv("HEROKU_API_KEY","HK543fklqxgt66hvxf")

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/STRIX01/V0.9",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv(
    "GIT_TOKEN", None
)  
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/Syphixlabs")
SUPPORT_GROUP = getenv("SUPPORT_GROUP", "https://t.me/syphixhub")
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", True))
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "2a230af10e0a40638dc77c1febb47170")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "7f92897a59464ddbbf00f06cd6bda7fc")
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 5242880000))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 5242880000))

STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)


BANNED_USERS = {}
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}


START_IMG_URL = getenv("START_IMG_URL", "https://files.catbox.moe/ard90z.jpg")
PING_IMG_URL = getenv("PING_IMG_URL", "https://files.catbox.moe/ard90z.jpg")
PLAYLIST_IMG_URL = "https://files.catbox.moe/ard90z.jpg"
STATS_IMG_URL = getenv("STATS_IMG_URL", "https://files.catbox.moe/ard90z.jpg")
TELEGRAM_AUDIO_URL = "https://files.catbox.moe/ard90z.jpg"
TELEGRAM_VIDEO_URL = "https://files.catbox.moe/ard90z.jpg"
STREAM_IMG_URL = "https://files.catbox.moe/ard90z.jpg"
SOUNCLOUD_IMG_URL = "https://files.catbox.moe/ard90z.jpg"
YOUTUBE_IMG_URL = "https://files.catbox.moe/ard90z.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://files.catbox.moe/ard90z.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://files.catbox.moe/ard90z.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://files.catbox.moe/ard90z.jpg"

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))


if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_GROUP:
    if not re.match("(?:http|https)://", SUPPORT_GROUP):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_GROUP url is wrong. Please ensure that it starts with https://"
        )







