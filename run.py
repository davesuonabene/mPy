import sys
import os
import uvicorn

# Add the 'src' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

if __name__ == "__main__":
    # Import the FastAPI app after setting the path
    from player_server.main import app
    uvicorn.run(app, host="0.0.0.0", port=8000)
