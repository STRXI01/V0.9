import asyncio
import os
import re
import json
from typing import Union
import yt_dlp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch
from Syphix.utils.database import is_on_off
from Syphix.utils.formatters import time_to_seconds
import logging
import aiohttp

async def shell_cmd(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, errorz = await proc.communicate()
    if errorz:
        if "unavailable videos are hidden" in (errorz.decode("utf-8")).lower():
            return out.decode("utf-8")
        else:
            return errorz.decode("utf-8")
    return out.decode("utf-8")

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        self.api_base = "https://honox-five.vercel.app"
        self.max_size_mb = 250

    def extract_video_id(self, link: str) -> str | None:
        pattern = r"(?:v=|youtu\.be/|youtube\.com/(?:embed/|v/|watch\?v=|shorts/))([0-9A-Za-z_-]{11})"
        match = re.search(pattern, link)
        return match.group(1) if match else None

    async def _get_api_info(self, video_id: str, quality: str = "mp3") -> dict | None:
        """Fetch JSON from API and return the response dict."""
        endpoint = "/mp3" if quality == "mp3" else "/download"
        params = f"?id={video_id}"
        if quality != "mp3":
            params += f"&format={quality}"
        url = f"{self.api_base}{endpoint}{params}"
        try:
            timeout = aiohttp.ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.json()
        except Exception as e:
            logging.error(f"API info fetch error: {e}")
        return None

    async def _get_file_size_from_url(self, download_url: str) -> int | None:
        """Get file size from HEAD request."""
        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.head(download_url) as response:
                    if response.status == 200:
                        content_length = response.headers.get("content-length")
                        return int(content_length) if content_length else None
        except Exception as e:
            logging.error(f"Size check error: {e}")
        return None

    async def _download_file_from_url(self, download_url: str, filepath: str) -> str | None:
        try:
            timeout = aiohttp.ClientTimeout(total=300)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(download_url) as response:
                    if response.status != 200:
                        logging.error(f"Download failed: {response.status}")
                        return None
                    content_length = response.headers.get("content-length")
                    if content_length:
                        size_bytes = int(content_length)
                        if size_bytes > self.max_size_mb * 1024 * 1024:
                            logging.warning(f"File too large ({size_bytes / (1024*1024):.1f} MB > {self.max_size_mb} MB)")
                            return None
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    with open(filepath, "wb") as f:
                        async for chunk in response.content.iter_chunked(8192):
                            f.write(chunk)
                    logging.info(f"Downloaded {filepath}")
                    return filepath
        except Exception as e:
            logging.error(f"File download error: {e}")
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except:
                    pass
            return None

    async def _fallback_audio_download(self, link: str) -> str:
        loop = asyncio.get_running_loop()
        def dl():
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=True)
                vid_id = info['id']
                ext = info.get('ext', 'webm')
                path = f"downloads/{vid_id}.{ext}"
                if os.path.exists(path):
                    return path
                return None
        return await loop.run_in_executor(None, dl)

    async def _fallback_video_download(self, link: str) -> str:
        loop = asyncio.get_running_loop()
        def dl():
            ydl_opts = {
                "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "merge_output_format": "mp4",
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
                vid_id = ydl.extract_info(link, download=False)['id']
                possible_paths = [f"downloads/{vid_id}.mp4", f"downloads/{vid_id}.mkv", f"downloads/{vid_id}.webm"]
                for p in possible_paths:
                    if os.path.exists(p):
                        return p
                return None
        return await loop.run_in_executor(None, dl)

    async def _fallback_direct_video_url(self, link: str) -> tuple[int, str]:
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "-g",
            "-f",
            "best[height<=?720][width<=?1280]",
            link,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode == 0 and stdout:
            return 1, stdout.decode().strip().split("\n")[0]
        return 0, stderr.decode() if stderr else "Unknown error"

    async def _custom_song_audio_dl(self, link: str, title: str, format_id: str | None) -> str | None:
        if not format_id:
            return None
        loop = asyncio.get_running_loop()
        def dl():
            safe_title = re.sub(r'[\\/:*?"<>|]', '_', str(title)).strip()[:100]
            fpath = f"downloads/{safe_title}.%(ext)s"
            ydl_opts = {
                "format": format_id,
                "outtmpl": fpath,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "prefer_ffmpeg": True,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            safe_title_no_ext = re.sub(r'[\\/:*?"<>|]', '_', str(title)).strip()[:100]
            mp3_path = f"downloads/{safe_title_no_ext}.mp3"
            if os.path.exists(mp3_path):
                return mp3_path
            return None
        return await loop.run_in_executor(None, dl)

    async def _custom_song_video_dl(self, link: str, title: str, format_id: str | None) -> str | None:
        if not format_id:
            return None
        loop = asyncio.get_running_loop()
        def dl():
            safe_title = re.sub(r'[\\/:*?"<>|]', '_', str(title)).strip()[:100]
            fpath = f"downloads/{safe_title}.%(ext)s"
            formats = f"{format_id}+140"
            ydl_opts = {
                "format": formats,
                "outtmpl": fpath,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "prefer_ffmpeg": True,
                "merge_output_format": "mp4",
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            mp4_path = f"downloads/{safe_title}.mp4"
            if os.path.exists(mp4_path):
                return mp4_path
            return None
        return await loop.run_in_executor(None, dl)

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        text = ""
        offset = None
        length = None
        for message in messages:
            if offset is not None:
                break
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        offset, length = entity.offset, entity.length
                        break
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        if offset is None:
            return None
        return text[offset : offset + length]

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            vidid = result["id"]
            duration_sec = 0 if str(duration_min) == "None" else int(time_to_seconds(duration_min))
            return title, duration_min, duration_sec, thumbnail, vidid
        return None, None, None, None, None

    async def title(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            return result["title"]
        return None

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            return result["duration"]
        return None

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            return result["thumbnails"][0]["url"].split("?")[0]
        return None

    async def video(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "-g",
            "-f",
            "best[height<=?720][width<=?1280]",
            link,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if stdout:
            return 1, stdout.decode().strip().split("\n")[0]
        return 0, stderr.decode() if stderr else "Unknown error"

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        if videoid:
            link = self.listbase + link
        if "&" in link:
            link = link.split("&")[0]
        playlist = await shell_cmd(
            f"yt-dlp -i --get-id --flat-playlist --playlist-end {limit} --skip-download {link}"
        )
        result = [id.strip() for id in playlist.split("\n") if id.strip()]
        return result

    async def track(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            vidid = result["id"]
            yturl = result["link"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            track_details = {
                "title": title,
                "link": yturl,
                "vidid": vidid,
                "duration_min": duration_min,
                "thumb": thumbnail,
            }
            return track_details, vidid
        return None, None

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        ytdl_opts = {"quiet": True}
        ydl = yt_dlp.YoutubeDL(ytdl_opts)
        formats_available = []
        try:
            with ydl:
                r = ydl.extract_info(link, download=False)
                for format_ in r["formats"]:
                    try:
                        fmt_str = str(format_["format"])
                        if "dash" in fmt_str.lower():
                            continue
                        if all(key in format_ for key in ["format", "filesize", "format_id", "ext", "format_note"]):
                            formats_available.append({
                                "format": format_["format"],
                                "filesize": format_["filesize"],
                                "format_id": format_["format_id"],
                                "ext": format_["ext"],
                                "format_note": format_["format_note"],
                                "yturl": link,
                            })
                    except (KeyError, TypeError):
                        continue
        except Exception as e:
            logging.error(f"Formats extraction error: {e}")
        return formats_available, link

    async def slider(self, link: str, query_type: int, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        a = VideosSearch(link, limit=10)
        result = (await a.next()).get("result", [])
        if query_type < len(result):
            res = result[query_type]
            title = res["title"]
            duration_min = res["duration"]
            vidid = res["id"]
            thumbnail = res["thumbnails"][0]["url"].split("?")[0]
            return title, duration_min, thumbnail, vidid
        return None, None, None, None

    async def download(
        self,
        link: str,
        mystic,  # unused, kept for compatibility
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ) -> Union[str, tuple[str, bool], None]:
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]

        video_id = self.extract_video_id(link)
        if not video_id:
            return None

        quality = "720" if video or songvideo else "mp3"

        # Priority: custom song with format_id -> yt-dlp custom
        if songvideo:
            if format_id:
                path = await self._custom_song_video_dl(link, title, format_id)
                if path:
                    return path
            # API
            api_info = await self._get_api_info(video_id, "1080" if format_id else "720")
            if api_info and "downloadUrl" in api_info:
                safe_title = re.sub(r'[\\/:*?"<>|]', '_', str(title or api_info.get("title", video_id))).strip()[:100]
                path = f"downloads/{safe_title}.mp4"
                path = await self._download_file_from_url(api_info["downloadUrl"], path)
                if path:
                    return path
            # yt-dlp fallback
            return await self._fallback_video_download(link)

        if songaudio:
            if format_id:
                path = await self._custom_song_audio_dl(link, title, format_id)
                if path:
                    return path
            # API
            api_info = await self._get_api_info(video_id, "mp3")
            if api_info and "downloadUrl" in api_info:
                safe_title = re.sub(r'[\\/:*?"<>|]', '_', str(title or api_info.get("title", video_id))).strip()[:100]
                path = f"downloads/{safe_title}.mp3"
                path = await self._download_file_from_url(api_info["downloadUrl"], path)
                if path:
                    return path
            # yt-dlp fallback
            return await self._fallback_audio_download(link)

        if video:
            api_info = await self._get_api_info(video_id, "720")
            if not api_info or "downloadUrl" not in api_info:
                # Fallback to yt-dlp
                if await is_on_off(1):
                    path = await self._fallback_video_download(link)
                    return path, True if path else None
                else:
                    status, url_or_err = await self._fallback_direct_video_url(link)
                    return (url_or_err, False) if status == 1 else None
            download_url = api_info["downloadUrl"]
            if await is_on_off(1):
                # Download to file
                path = f"downloads/{video_id}.mp4"
                path = await self._download_file_from_url(download_url, path)
                return path, True if path else None
            else:
                # Check size for direct URL
                file_size = await self._get_file_size_from_url(download_url)
                if file_size and file_size > self.max_size_mb * 1024 * 1024:
                    # Too large, download instead
                    path = f"downloads/{video_id}.mp4"
                    path = await self._download_file_from_url(download_url, path)
                    return path, True if path else None
                return download_url, False

        # Default: audio, download to file
        api_info = await self._get_api_info(video_id, "mp3")
        if api_info and "downloadUrl" in api_info:
            path = f"downloads/{video_id}.mp3"
            path = await self._download_file_from_url(api_info["downloadUrl"], path)
            if path:
                return path, True
        # Fallback
        path = await self._fallback_audio_download(link)
        return path, True if path else None
