import os
from fastapi import FastAPI, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from pydantic import BaseModel

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

class PlayRequest(BaseModel):
    file_path: str

class VolumeUpdateRequest(BaseModel):
    volume: float

class SeekRequest(BaseModel):
    position: float

@app.post("/api/v1/play")
async def play_track(request: PlayRequest):
    absolute_file_path = Path.cwd() / request.file_path
    if not absolute_file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    try:
        player_instance.play(str(absolute_file_path))
        return {"status": "playing", "file": str(absolute_file_path)}
    except Exception as e:
        print(f"ERROR: Failed to play track: {e}") # Added logging
        raise HTTPException(status_code=500, detail=f"Failed to play track: {e}")


@app.post("/api/v1/stop")
async def stop_track():
    try:
        player_instance.stop()
        return {"status": "stopped"}
    except Exception as e:
        print(f"ERROR: Failed to stop track: {e}") # Added logging
        raise HTTPException(status_code=500, detail=f"Failed to stop track: {e}")

@app.get("/api/v1/status")
async def get_playback_status():
    try:
        current_track_title = None
        if player_instance.current_track:
            current_track_title = Path(player_instance.current_track).name
        return {
            "is_playing": player_instance.system.is_playing,
            "current_position": player_instance.get_current_position(),
            "duration": player_instance.get_duration(),
            "current_track_title": current_track_title
        }
    except Exception as e:
        print(f"ERROR: Failed to get playback status: {e}") # Added logging
        raise HTTPException(status_code=500, detail=f"Failed to get playback status: {e}")

@app.post("/api/v1/volume")
async def set_volume(request: VolumeUpdateRequest):
    try:
        player_instance.set_volume(request.volume)
        return {"status": "volume set", "volume": request.volume}
    except ValueError as e:
        print(f"ERROR: Invalid volume value: {e}") # Added logging
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"ERROR: Failed to set volume: {e}") # Added logging
        raise HTTPException(status_code=500, detail=f"Failed to set volume: {e}")


@app.get("/api/v1/volume")
async def get_volume():
    try:
        volume = player_instance.get_volume()
        return {"volume": volume}
    except Exception as e:
        print(f"ERROR: Failed to get volume: {e}") # Added logging
        raise HTTPException(status_code=500, detail=f"Failed to get volume: {e}")


@app.post("/api/v1/mute")
async def mute_audio():
    try:
        player_instance.mute()
        return {"status": "muted"}
    except Exception as e:
        print(f"ERROR: Failed to mute audio: {e}") # Added logging
        raise HTTPException(status_code=500, detail=f"Failed to mute audio: {e}")


@app.post("/api/v1/unmute")
async def unmute_audio():
    try:
        player_instance.unmute()
        return {"status": "unmuted"}
    except Exception as e:
        print(f"ERROR: Failed to unmute audio: {e}") # Added logging
        raise HTTPException(status_code=500, detail=f"Failed to unmute audio: {e}")

@app.post("/api/v1/seek")
async def seek_track(request: SeekRequest):
    try:
        player_instance.seek(request.position)
        return {"status": "seeking", "position": request.position}
    except Exception as e:
        print(f"ERROR: Failed to seek track: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to seek track: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
