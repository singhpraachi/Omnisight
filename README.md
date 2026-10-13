# Omnisight
Multimodal UI Self-Healing and RPA Agent

## Project Overview

OmniSight is a multimodal UI self-healing and RPA agent designed
to detect visual UI issues, analyze screenshots and DOM information,
and assist in generating UI fixes.

## Team

- Praachi — Team Lead
- Vishwas — Team Member

## API Setup

### Run the API

Activate the Python virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Start the FastAPI server from the project root:

```powershell
python -m uvicorn api.main:app --reload
```

### Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check API health |
| POST | `/webhook` | Receive and validate a CI/CD webhook |

### API Documentation

With the server running, visit:

- Interactive API docs: `http://127.0.0.1:8000/docs`
- OpenAPI schema: `http://127.0.0.1:8000/openapi.json`

### Run Tests

```powershell
python -m pytest -v
```

The tests cover API health, valid webhook requests, invalid URLs, and missing required fields.
