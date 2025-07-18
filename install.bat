@echo off
echo.
echo ========================================
echo  ComfyUI Video Generator - Installer
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python non trovato. Installazione in corso...
    echo Scaricando Python...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe' -OutFile 'python-installer.exe'"
    echo Installando Python...
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python-installer.exe
    echo Python installato!
)

REM Run Python installer
echo Avvio installazione automatica...
python setup.py

echo.
echo Installazione completata!
echo.
echo Per avviare l'app, esegui: start.bat
echo.
pause