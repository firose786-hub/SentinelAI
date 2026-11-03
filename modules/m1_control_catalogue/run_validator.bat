@echo off
cd /d "%~dp0"
title SentinelAI - Module 1 (M1) Catalogue Validator
color 0a

echo =====================================================================
echo       RUNNING SENTINELAI M1 CONTROL CATALOGUE VALIDATION
echo =====================================================================
echo Current Directory: %CD%
echo.

set PYCMD=python
where python >nul 2>&1
if %errorlevel% neq 0 (
    set PYCMD=py
)

%PYCMD% validator.py

echo.
pause
