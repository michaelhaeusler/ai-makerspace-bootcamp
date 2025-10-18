# InsuranceLens Backend

Modern Python FastAPI backend using uv for dependency management.

## Quick Start

```bash
# Install dependencies (creates .venv automatically)
uv sync

# Start the development server
uv run uvicorn app.main:app --reload

# Visit http://localhost:8000/docs for API documentation
```

## Development Commands

```bash
# Run tests
uv run pytest

# Format code
uv run black app/
uv run isort app/

# Type checking
uv run mypy app/

# Add new dependencies
uv add package-name

# Add development dependencies
uv add --dev package-name
```

## For pip Users

If you don't have `uv` installed, you can still use pip:

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install from pyproject.toml
pip install -e .

# Or install dependencies manually
pip install fastapi "uvicorn[standard]" openai langchain langchain-openai langgraph langsmith qdrant-client tiktoken pypdf pymupdf tavily-python python-multipart python-dotenv pydantic httpx tenacity pytest pytest-asyncio black isort mypy
```

## Project Structure

```
app/
├── __init__.py
├── main.py              # FastAPI application
├── core/
│   ├── __init__.py
│   └── config.py        # Settings and configuration
├── models/
│   ├── __init__.py
│   └── schemas.py       # Pydantic models
├── api/
│   ├── __init__.py
│   └── routes/          # API endpoints
│       ├── __init__.py
│       ├── health.py    # Health checks
│       ├── policies.py  # Policy management
│       └── questions.py # Q&A endpoints
├── services/            # Business logic (to be implemented)
└── agents/              # LangGraph agents (to be implemented)
```
