@echo off
echo ========================================
echo  ComfyUI Video Generator - Stopping...
echo ========================================
echo.

echo Stopping Backend...
taskkill /f /im python.exe /fi "WINDOWTITLE eq ComfyUI Video Generator - Backend*" 2>nul

echo Stopping Frontend...
taskkill /f /im node.exe /fi "WINDOWTITLE eq ComfyUI Video Generator - Frontend*" 2>nul

echo.
echo ========================================
echo  ComfyUI Video Generator Stopped!
echo ========================================
echo.
pause