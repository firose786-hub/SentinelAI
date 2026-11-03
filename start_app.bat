@echo off
cd /d "%~dp0"
title SentinelAI Enterprise Platform Launcher
color 0b

echo =====================================================================
echo           SENTINELAI ENTERPRISE SOC PLATFORM LAUNCHER
echo =====================================================================
echo Current Directory: %CD%
echo.

set PYCMD=python
where python >nul 2>&1
if %errorlevel% neq 0 (
    set PYCMD=py
)

echo [1/2] Launching FastAPI Backend (Port 8000)...
start "SentinelAI Backend (FastAPI)" /min cmd /c "%PYCMD% -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000"

timeout /t 2 /nobreak >nul

echo [2/2] Launching Streamlit Frontend (Port 8501)...
echo.
echo Opening http://localhost:8501 in your browser...
echo (Keep this black window OPEN while using the platform)
echo =====================================================================
echo.

%PYCMD% -m streamlit run app.py --server.port 8501

if %errorlevel% neq 0 (
    echo.
    echo Streamlit exited with error code %errorlevel%.
    echo Trying fallback directly with frontend/app.py...
    %PYCMD% -m streamlit run frontend/app.py --server.port 8501
)

echo.
echo =====================================================================
echo Server stopped.
pause
