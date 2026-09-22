import uvicorn
from app.config import PORT, HOST

if __name__ == "__main__":
    print(f"Starting Smart Code Inspection Platform on http://localhost:{PORT}")
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
