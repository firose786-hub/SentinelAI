"""
Root Streamlit launcher
Run via: streamlit run app.py
"""
import runpy
from pathlib import Path

frontend_app = Path(__file__).resolve().parent / "frontend" / "app.py"
runpy.run_path(str(frontend_app), run_name="__main__")
