"""
Root Streamlit launcher
Run via: streamlit run app.py
"""
import sys
import runpy
from pathlib import Path

root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

frontend_app = root_dir / "frontend" / "app.py"
runpy.run_path(str(frontend_app), run_name="__main__")
