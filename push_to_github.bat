@echo off
title Uploading to firose786-hub/SentinelAI
color 0a

echo =====================================================================
echo    PUSHING LATEST SENTINELAI CODE TO firose786-hub/SentinelAI
echo =====================================================================
echo.

git init
git remote remove origin 2>nul
git remote add origin https://github.com/firose786-hub/SentinelAI.git
git branch -M main

echo [1/3] Staging all files and new folders...
git add .

echo [2/3] Creating commit...
git commit -m "Upload SentinelAI Enterprise Platform: 12 Agents, RBAC & SOC Dashboards"

echo [3/3] Pushing to GitHub repository (firose786-hub/SentinelAI)...
git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo -----------------------------------------------------------------
    echo [NOTE] If push was rejected because remote has existing commits,
    echo pulling and merging or using force push...
    echo -----------------------------------------------------------------
    git push -u origin main --force
)

echo.
echo =====================================================================
echo Done! Please check https://github.com/firose786-hub/SentinelAI
echo =====================================================================
pause
