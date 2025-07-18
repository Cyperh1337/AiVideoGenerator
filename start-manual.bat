@echo off
echo ========================================
echo  ComfyUI Video Generator - Manual Start
echo ========================================
echo.

echo STEP 1: Starting Backend...
echo.
echo In una nuova finestra del terminale, esegui:
echo cd "%~dp0backend"
echo python server.py
echo.
pause

echo STEP 2: Starting Frontend...
echo.
echo In un'altra finestra del terminale, esegui:
echo cd "%~dp0frontend"
echo npm start
echo.
pause

echo STEP 3: Accesso App
echo.
echo Apri il browser e vai su: http://localhost:3000
echo.
echo IMPORTANTE: Assicurati che ComfyUI sia in esecuzione su:
echo http://127.0.0.1:8188
echo.
start http://localhost:3000
pause