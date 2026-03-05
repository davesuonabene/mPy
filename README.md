# mPy - Media Server Py

## Project Scope
A Python-based MP3 player server with a web UI and a REST API. The server will enable users to browse, play, and manage their music collection via a web interface, while also providing a fully accessible REST API for programmatic control by agents (like myself).

## First Steps
1.  **Create and activate a Python virtual environment** .
2.  **Install project dependencies** within the virtual environment.
3.  Implement the basic folder structure.
4.  Create a simple "Hello World" endpoint for the REST API (already done in `src/player_server/main.py`).
5.  Develop a minimal web page to interact with the API.
6.  **Run the FastAPI server** .

## Development Setup and Running the Server

To get the MP3 player server up and running for development:

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone <your-repo-url>
    cd mp3-player-server
    ```

2.  **Create and activate a virtual environment** :
    ```bash
    python -m venv .venv
    source ./.venv/bin/activate
    ```

3.  **Install dependencies** :
    ```bash
    pip install -e .
    ```

4.  **Run the FastAPI server** :
    ```bash
    python -m player_server.main
    ```
    The server will be accessible at `http://127.0.0.1:8000` (or `http://localhost:8000`). You can test the basic `health` endpoint by navigating to `http://127.0.0.1:8000/health` in your browser or using `curl` :
    ```bash
    curl http://127.0.0.1:8000/health
    ```

## Agent-Driven Architecture Notes
Based on research into "AI Agent Implementation - Technical Documentation" by mc095 (https://mc095.github.io/jsonparser/ai-agent.html), our project will closely follow a service-oriented architecture designed for agent accessibility.

Key principles from this research include:
-   **Service-Oriented `src` Layout**: Reinforces the separation of concerns between core logic, API, and web UI.
-   **Core Agent Logic (e.g., `core/player.py`, `core/library.py`)**: These modules will encapsulate the intelligent decision-making and orchestration of music management, analogous to an AI agent's core processing.
-   **FastAPI for API Entry Point (`src/player_server/main.py`, `src/player_server/api/`)**: Provides clear, self-documenting API endpoints for both human-controlled web UI and programmatic access by AI agents.
-   **SQLite with SQLAlchemy (`src/player_server/models/`)**: Manages persistent data for music metadata, playlists, and potentially agent-specific memory.
-   **Frontend (`src/player_server/web/static/`, `src/player_server/web/templates/`)**: A modular web interface to interact with the API.
-   **Enhanced Agent Accessibility**: Emphasis on `AGENTS.md` for explicit instructions to AI agents, type hinting for static analysis, and leveraging FastAPI's auto-generated API documentation (Swagger/OpenAPI).

This architecture ensures a robust, extensible, and understandable system for both developers and AI agents.

## Dependencies
*   Python 3.x
*   FastAPI (web framework, REST API)
*   Uvicorn (ASGI server for FastAPI)
*   SQLite (built-in, used via SQLAlchemy ORM)
*   Mutagen (reading/writing MP3 tags)

*   A front-end framework (e.g., HTML, CSS, JavaScript; or a lightweight JS framework to be determined).

## Recommended Folder Structure
The design prioritizes a **Service-Oriented `src` Layout** for clear separation of concerns, making it easy to understand where business logic ends and transport layers (Web/API) begin.

```text
mp3-player-server/
├── .github/                # CI/CD workflows
├── docs/                   # Detailed documentation
│   ├── ARCHITECTURE.md     # High-level design decisions
│   └── API_SPEC.md         # Manual API notes (if not using Swagger)
├── src/
│   └── player_server/      # Main package
│       ├── api/            # REST API layer (FastAPI/Flask routes)
│       │   ├── v1/         # Versioned endpoints
│       │   └── dependencies.py
│       ├── web/            # Web UI layer
│       │   ├── static/     # CSS, JS, Images
│       │   └── templates/  # Jinja2/HTML templates
│       ├── core/           # Core Business Logic (The "Brain")
│       │   ├── player.py   # Audio playback logic
│       │   ├── library.py  # MP3 scanning and indexing
│       │   └── config.py   # Settings and env vars
│       ├── models/         # Data schemas (Pydantic/SQLAlchemy)
│       │   ├── track.py
│       │   └── playlist.py
│       ├── services/       # External Integrations
│       │   ├── audio_os.py # Hardware-level audio interface
│       │   └── database.py # Persistence layer
│       ├── utils/          # Shared helpers (logging, formatting)
│       ├── __init__.py
│       └── main.py         # Application entry point
├── tests/                  # Test suite mirroring src/ structure
│   ├── unit/
│   └── integration/
├── data/                   # Default local storage (db, logs)
├── scripts/                # Setup/Maintenance scripts
├── .env.example            # Template for environment variables
├── pyproject.toml          # Modern Python build/dependency config
├── README.md               # User-facing overview
└── AGENTS.md               # Specific instructions for AI Agents
```

## Implemented Foundational Components

### `AGENTS.md`
A dedicated `AGENTS.md` file has been created at the project root. This file provides clear instructions and guidelines for AI agents interacting with the codebase, covering architectural overview, development constraints (e.g., type hinting, unit tests, PEP 8), and areas of focus.

### `src/player_server/core/config.py`
This file now contains a `Settings` class leveraging `pydantic-settings`. It defines core application configurations such as `PROJECT_NAME`, `DATABASE_URL` (pointing to `sqlite:///./data/mpy_data.db`), and `MUSIC_DIRECTORY` (`./data/music`), with support for `.env` files.

### `src/player_server/services/database.py`
This module sets up the SQLAlchemy engine for SQLite, a `sessionmaker` for database sessions, and a `declarative_base` for ORM models. It also includes a `get_db` dependency function for FastAPI to manage database sessions.

### Key Architectural Decisions
1.  **Separation of Concerns**: The `core/` directory holds the fundamental logic of the MP3 player, independent of how it's accessed. `api/` and `web/` act as adapters, exposing this core logic. This modularity allows for isolated changes without ripple effects across different layers.
2.  **The `src` Layout**: Adopting a `src/` folder is a Python best practice, ensuring clean imports and proper package structuring.
3.  **Agent Accessibility Features**:
    *   **`AGENTS.md`**: A dedicated file will contain codebase maps, naming conventions (e.g., "always use type hints"), and critical areas to avoid or be cautious with.
    *   **Type Hinting**: Essential for static analysis, enabling better code completion and error detection for agents.
    *   **Self-Documenting API**: Using a framework like FastAPI (or a similar approach with Flask) will automatically generate API documentation (e.g., Swagger), which agents can parse to understand server interactions.
4.  **Hardware Abstraction**: The `services/audio_os.py` file will abstract the audio playback library, making it easy to swap out different audio interfaces if needed, with minimal impact on other parts of the system.
5.  **Direct Backend Audio Playback (Robust Streaming Library)**: Audio is rendered directly through the host PC's audio hardware via the `miniaudio` robust streaming library running inside the FastAPI server process. We explicitly avoid `pygame`/SDL2 for the core audio engine due to its tendency to lose the active audio sink (ALSA/PulseAudio/PipeWire) when running headless behind a web server. The web UI and API act as a lightweight remote control rather than the audio sink, enabling seamless physical audio system integration.

### Agent Implementation Notes
*   **March 5, 2026**: The migration from `pygame` to `miniaudio` as the core audio engine was successfully completed. The project now relies on `miniaudio` for robust hardware-level audio playback.
