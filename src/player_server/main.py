import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from player_server.core.player import player_instance

app = FastAPI()

# Paths relative to project root
MUSIC_DIR = Path("data/music")
STATIC_DIR = Path("src/player_server/web/static")
TEMPLATES_DIR = Path("src/player_server/web/templates")

# Ensure directories exist for robustness
MUSIC_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/")
async def get_index():
    return FileResponse(str(TEMPLATES_DIR / "index.html"))

@app.get("/api/v1/tracks")
async def get_tracks():
    tracks = []
    if MUSIC_DIR.exists():
        # Get all .mp3 files, sorted alphabetically
        mp3_files = sorted([f for f in os.listdir(MUSIC_DIR) if f.endswith('.mp3')])
        for i, filename in enumerate(mp3_files):
            file_path = MUSIC_DIR / filename
            tracks.append({
                "id": i + 1,
                "title": filename,
                "file_path": str(file_path)
            })
    return tracks

from pydantic import BaseModel

class PlayRequest(BaseModel):
    file_path: str

@app.post("/api/v1/play")
async def play_track(request: PlayRequest):
    absolute_file_path = Path.cwd() / request.file_path
    if not absolute_file_path.exists():
        return {"error": "File not found"}
    player_instance.play(str(absolute_file_path))
    return {"status": "playing", "file": str(absolute_file_path)}

@app.post("/api/v1/stop")
async def stop_track():
    player_instance.stop()
    return {"status": "stopped"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
