# ----------------- FIX FOR ASYNCIO + UVLOOP -----------------
import asyncio

# Try enabling uvloop if installed
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except Exception:
    pass

# Make sure the main thread has an event loop
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())
# ------------------------------------------------------------


from Syphix.core.bot import AMBOT
from Syphix.core.dir import dirr
from Syphix.core.git import git
from Syphix.core.userbot import Userbot
from Syphix.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = AMBOT()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
