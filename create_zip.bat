@echo off
cd /d "%~dp0"
title SentinelAI Project ZIP Generator
color 0b

echo =====================================================================
echo           SENTINELAI ENTERPRISE - CREATE COMPLETE ZIP FILE
echo =====================================================================
echo Current Directory: %CD%
echo.

set PYCMD=python
where python >nul 2>&1
if %errorlevel% neq 0 (
    set PYCMD=py
)

echo Running ZIP generator script...
%PYCMD% create_zip.py

if %errorlevel% neq 0 (
    echo.
    echo Python packaging had an issue. Falling back to PowerShell Compress-Archive...
    powershell -Command "Compress-Archive -Path * -DestinationPath ..\SentinelAI_MajorProject_Complete.zip -Force"
    echo [DONE] PowerShell generated ..\SentinelAI_MajorProject_Complete.zip
)

echo.
echo =====================================================================
echo ZIP file created successfully in your parent folder:
echo E:\3-2AllSub\4-1majorProject\SentinelAI_MajorProject_Complete.zip
echo =====================================================================
echo.
pause
