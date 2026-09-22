import uvicorn
from backend.app.config import HOST, PORT

def main():
    print("==========================================================================")
    print(" 🛡️ SentinelAI — Agentic Smart Compliance Auditor & AI Security Platform")
    print(f" FastAPI Backend running at: http://{HOST}:{PORT}")
    print(" Interactive Swagger Docs at: http://localhost:8000/docs or http://localhost:5000/docs")
    print(" To launch the Streamlit Dashboard, run: streamlit run frontend/app.py")
    print("==========================================================================")
    uvicorn.run("backend.app.main:app", host=HOST, port=PORT, reload=True)

if __name__ == "__main__":
    main()
