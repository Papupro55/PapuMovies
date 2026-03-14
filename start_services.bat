@echo off
REM PapuMovies Microservices Startup Script for Windows

echo.
echo ========================================
echo PapuMovies - Microservices Startup
echo ========================================
echo.
echo This script will open 4 terminal windows to run the services:
echo - Movie Service (Port 5001)
echo - Rating Service (Port 5002)
echo - Trailer Service (Port 5003)
echo - Frontend Service (Port 5000)
echo.
echo Prerequisites:
echo - Python 3.8+ installed
echo - All dependencies installed (pip install -r requirements.txt)
echo.
pause

REM Get the current directory
setlocal enabledelayedexpansion
set SCRIPT_DIR=%~dp0

REM Open Movie Service
echo Starting Movie Service...
start cmd /k "cd /d !SCRIPT_DIR!movie-service && python app.py"
timeout /t 2

REM Open Rating Service
echo Starting Rating Service...
start cmd /k "cd /d !SCRIPT_DIR!rating-service && python app.py"
timeout /t 2

REM Open Trailer Service
echo Starting Trailer Service...
start cmd /k "cd /d !SCRIPT_DIR!trailer-service && python app.py"
timeout /t 2

REM Open Frontend Service
echo Starting Frontend Service...
start cmd /k "cd /d !SCRIPT_DIR!frontend && python app.py"

echo.
echo All services should be starting...
echo.
echo Access the application at: http://localhost:5000
echo.
echo Services:
echo - Movie Service: http://localhost:5001
echo - Rating Service: http://localhost:5002
echo - Trailer Service: http://localhost:5003
echo - Frontend: http://localhost:5000
echo.
