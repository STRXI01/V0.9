import os
import time
import json
import asyncio
import aiohttp

from config import COOKIE_URL

COOKIE_PATH = "Syphix/assets/cookies.txt"
TIMESTAMP_PATH = "Syphix/assets/cookie_time.json"
REFRESH_INTERVAL = 48 * 60 * 60  # 48 hours


def resolve_raw_cookie_url(url: str) -> str:
    """Convert Pastebin/Batbin URLs to raw endpoints if needed."""
    url = url.strip()
    low_url = url.lower()
    if "pastebin.com/" in low_url and "/raw/" not in low_url:
        return f"https://pastebin.com/raw/{url.split('/')[-1]}"
    if "batbin.me/" in low_url and "/raw/" not in low_url:
        return f"https://batbin.me/raw/{url.split('/')[-1]}"
    return url


def _needs_refresh() -> bool:
    """Check if refresh interval hours passed since last refresh."""
    if not os.path.exists(TIMESTAMP_PATH):
        return True
    try:
        with open(TIMESTAMP_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        last_refresh = float(data.get("last_refresh", 0))
    except Exception:
        return True
    return (time.time() - last_refresh) >= REFRESH_INTERVAL


def _update_refresh_time():
    """Update timestamp JSON file."""
    try:
        data = {"last_refresh": time.time()}
        with open(TIMESTAMP_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except:
        pass


async def fetch_and_store_cookies(force: bool = False):
    """Fetch cookies, save, and restart bot if refreshed."""
    if not COOKIE_URL:
        raise EnvironmentError("⚠️ COOKIE_URL not set in env")

    if not force and not _needs_refresh() and os.path.exists(COOKIE_PATH):
        return

    raw_url = resolve_raw_cookie_url(COOKIE_URL)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(raw_url) as resp:
                if resp.status != 200:
                    raise ConnectionError(f"Failed to fetch cookies: {resp.status}")
                cookies = (await resp.text()).strip()
        except Exception as e:
            raise ConnectionError(f"⚠️ Can't fetch cookies: {e}")

    if not cookies.startswith("# Netscape"):
        raise ValueError("⚠️ Invalid cookie format (needs Netscape format).")
    if len(cookies) < 100:
        raise ValueError("⚠️ Cookie content too short. Possibly invalid.")

    try:
        if os.path.exists(COOKIE_PATH):
            os.remove(COOKIE_PATH)
        with open(COOKIE_PATH, "w", encoding="utf-8") as f:
            f.write(cookies)
        _update_refresh_time()
    except Exception as e:
        raise IOError(f"⚠️ Failed to save cookies: {e}")

    os.system(f"kill -9 {os.getpid()} && bash start")
