# Agent Instructions for mPy

## Architecture Overview
- **Service Layer**: All hardware or DB interactions MUST go through `services/`.
- **Core Logic**: Business rules (playback state, library indexing) reside in `core/`.
- **API**: FastAPI is used for the transport layer.

## Development Constraints
- Use type hints for all function signatures.
- Add unit tests in `tests/unit/` for any new logic in `core/`.
- Follow the PEP 8 style guide.
