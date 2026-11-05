@echo off
cd /d "%~dp0"
title SentinelAI - Automated Test Suite Runner
color 0a

echo =====================================================================
echo           SENTINELAI ENTERPRISE - AUTOMATED TEST SUITE
echo =====================================================================
echo Current Directory: %CD%
echo.

set PYCMD=python
where python >nul 2>&1
if %errorlevel% neq 0 (
    set PYCMD=py
)

echo [1/3] Running Module 1 Integrity Validator...
%PYCMD% modules/m1_control_catalogue/validator.py

echo.
echo [2/3] Running Pytest Unit & Integration Test Suites...
%PYCMD% -m pytest backend/tests -v --tb=short

if %errorlevel% equ 0 (
    echo.
    echo =====================================================================
    echo [SUCCESS] ALL TESTS PASSED SUCCESSFULLY!
    echo =====================================================================
) else (
    echo.
    echo [WARNING] Some tests encountered issues. Review log output above.
)

echo.
echo [3/3] Test Execution Completed.
echo.
pause
