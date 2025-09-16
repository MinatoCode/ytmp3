import os
import json
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
import yt_dlp

app = FastAPI()

# Vercel writable folder
DOWNLOAD_DIR = "/tmp"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Path to optional cookies file (if provided)
COOKIES_PATH = os.path.join(DOWNLOAD_DIR, "cookies.json")


def download_youtube_mp3(url: str, cookies: str = None) -> str:
    """
    Download YouTube video as MP3 and return the file path
    :param url: YouTube video URL
    :param cookies: Optional JSON string of cookies
    """
    # Save cookies if provided
    cookiefile = None
    if cookies:
        try:
            cookies_data = json.loads(cookies)
            with open(COOKIES_PATH, "w") as f:
                json.dump(cookies_data, f)
            cookiefile = COOKIES_PATH
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid cookies JSON: {e}")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "256",  # 256 kbps audio
        }],
        "quiet": True,
        "noplaylist": True,
        "cookiefile": cookiefile,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "unknown")
            mp3_file = os.path.join(DOWNLOAD_DIR, f"{title}.mp3")
            if os.path.exists(mp3_file):
                return mp3_file
            else:
                raise FileNotFoundError("MP3 file not found after download")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/ytmp3")
def api_ytmp3(
    url: str = Query(..., description="YouTube video URL"),
    cookies: str = Query(None, description="Optional JSON string of YouTube cookies")
):
    """
    Download YouTube video as MP3 and trigger auto-download in browser
    """
    mp3_path = download_youtube_mp3(url, cookies)

    return FileResponse(
        mp3_path,
        media_type="audio/mpeg",
        filename=os.path.basename(mp3_path),
        headers={"Content-Disposition": f'attachment; filename="{os.path.basename(mp3_path)}"'}
    )
    
