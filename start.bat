@echo off
echo ========================================
echo  ComfyUI Video Generator - Starting...
echo ========================================
echo.

echo Starting Backend Server...
cd /d "%~dp0backend"
start "ComfyUI Video Generator - Backend" python server.py

echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo Starting Frontend...
cd /d "%~dp0frontend"
start "ComfyUI Video Generator - Frontend" npm start

echo.
echo ========================================
echo  ComfyUI Video Generator Started!
echo ========================================
echo.
echo Backend API: http://localhost:8001
echo Frontend:    http://localhost:3000
echo.
echo IMPORTANTE: Assicurati che ComfyUI sia in esecuzione su:
echo http://127.0.0.1:8188
echo.
echo Premi un tasto per aprire il browser...
pause > nul
start http://localhost:3000