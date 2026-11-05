# SentinelAI — Installation & Setup Guide

**Project**: *SentinelAI — Agentic AI-Based Smart Compliance Auditor & AI Security Validation Platform for Enterprise LLM Systems*  
**Supported OS**: Windows 10/11, Linux (Ubuntu 22.04+), macOS  
**Target Directory**: `E:\3-2AllSub\4-1majorProject\sentinelaiMajorProject`  

---

## 1. Prerequisites

- **Python**: Version 3.11, 3.12, or 3.13 (Python 3.11+ 64-bit recommended).
- **Git**: Installed and added to system `PATH`.
- **System Memory**: Minimum 4 GB RAM (8 GB recommended).
- **Disk Space**: ~250 MB free disk space.

---

## 2. Quickstart (1-Click Launch on Windows)

In Windows File Explorer, open:
`E:\3-2AllSub\4-1majorProject\sentinelaiMajorProject`

1. **Launch Platform**: Double-click **`start_app.bat`**.
   - Starts FastAPI on `http://localhost:8000`.
   - Starts Streamlit on `http://localhost:8501`.
   - Automatically opens your default browser to `http://localhost:8501`.
2. **Run Tests**: Double-click **`run_tests.bat`**.
3. **Verify Module 1**: In `modules/m1_control_catalogue/`, double-click **`run_validator.bat`**.

---

## 3. Manual Step-by-Step Installation

### Step 1: Open Terminal & Navigate to Directory
```bash
cd "E:\3-2AllSub\4-1majorProject\sentinelaiMajorProject"
```

### Step 2: (Optional but Recommended) Create Virtual Environment
```bash
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Windows CMD:
.\venv\Scripts\activate.bat
```

### Step 3: Install Required Dependencies
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Environment Configuration
Copy `.env.example` to `.env`:
```bash
copy .env.example .env
```
*(Optional)* Add your Google Gemini API Key inside `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
PORT=8000
HOST=0.0.0.0
```
> **Note**: If `GEMINI_API_KEY` is omitted or empty, SentinelAI automatically operates in **100% deterministic offline fallback mode**.

### Step 5: Start the Application

#### Terminal 1 (Backend API):
```bash
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Terminal 2 (Streamlit Frontend):
```bash
streamlit run app.py
```
Open your web browser at: **`http://localhost:8501`**

---

## 4. Troubleshooting Common Issues

### Issue 1: `Port 8501 or 8000 Already in Use`
- **Solution**: Open Command Prompt as Administrator and run:
  ```cmd
  netstat -ano | findstr :8501
  taskkill /PID <PID_NUMBER> /F
  ```
  Or change the port: `streamlit run app.py --server.port 8502`.

### Issue 2: `ModuleNotFoundError`
- **Solution**: Ensure your working directory is the project root `E:\3-2AllSub\4-1majorProject\sentinelaiMajorProject` and that `pip install -r requirements.txt` has completed.

### Issue 3: `EPERM / Symlinks Not Supported on Windows`
- **Solution**: Windows standard mode handles file execution via direct paths without symlinks. `start_app.bat` handles this automatically using `cd /d "%~dp0"`.
