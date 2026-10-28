@echo off
title Green Building Performance Dashboard Server
echo ==========================================================
echo    GREEN BUILDING PERFORMANCE DASHBOARD LAUNCHER
echo ==========================================================
echo.
echo Starting Flask web server in the background...

cd /d "%~dp0\..\backend"
start "EcoBuildServer" cmd /k py app.py

echo Waiting for backend API to initialize (3 seconds)...
timeout /t 3 /nobreak > nul

echo Launching dashboard in maximized full-screen mode...
where chrome.exe >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    start "" "chrome.exe" --start-maximized --window-size=1920,1080 --app=http://127.0.0.1:5000
) else (
    where msedge.exe >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        start "" "msedge.exe" --start-maximized --window-size=1920,1080 --app=http://127.0.0.1:5000
    ) else (
        start http://127.0.0.1:5000
    )
)

echo.
echo ==========================================================
echo  Dashboard is active at http://127.0.0.1:5000
echo  Keep the EcoBuildServer window open while using the app.
echo  Close the EcoBuildServer window to stop the server.
echo ==========================================================
