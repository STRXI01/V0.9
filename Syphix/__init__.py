# ----------------- ASYNCIO + UVLOOP BOOTSTRAP (MUST BE FIRST) -----------------
import asyncio

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except Exception:
    pass

try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())
# ---------------------------------------------------------------------------

# ---- rest of file follows ----
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
