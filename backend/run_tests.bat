@echo off
cd /d "%~dp0"
title SentinelAI Backend Pytest Runner
color 0b

echo =====================================================================
echo           RUNNING SENTINELAI BACKEND PYTEST SUITE
echo =====================================================================
echo.

set PYCMD=python
where python >nul 2>&1
if %errorlevel% neq 0 (
    set PYCMD=py
)

cd ..
%PYCMD% -m pytest backend/tests -v

echo.
pause
