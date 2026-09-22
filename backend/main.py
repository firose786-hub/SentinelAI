"""
Main entrypoint shim for Uvicorn execution
Supports: uvicorn backend.main:app --reload --port 8000
"""

from backend.app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
