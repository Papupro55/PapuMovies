# PapuMovies Microservices Startup Script for PowerShell

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PapuMovies - Microservices Startup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "This script will start 4 services:" -ForegroundColor Yellow
Write-Host "- Movie Service (Port 5001)" -ForegroundColor Yellow
Write-Host "- Rating Service (Port 5002)" -ForegroundColor Yellow
Write-Host "- Trailer Service (Port 5003)" -ForegroundColor Yellow
Write-Host "- Frontend Service (Port 5000)" -ForegroundColor Yellow
Write-Host ""

Write-Host "Prerequisites:" -ForegroundColor Yellow
Write-Host "- Python 3.8+ installed" -ForegroundColor Yellow
Write-Host "- All dependencies installed (pip install -r requirements.txt)" -ForegroundColor Yellow
Write-Host ""

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Function to start a service
function Start-Service {
    param(
        [string]$serviceName,
        [string]$port,
        [string]$serviceDir
    )
    
    Write-Host "Starting $serviceName on port $port..." -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$serviceDir'; python app.py" -WindowStyle Normal
    Start-Sleep -Seconds 2
}

# Start all services
Start-Service -serviceName "Movie Service" -port "5001" -serviceDir "$scriptDir\movie-service"
Start-Service -serviceName "Rating Service" -port "5002" -serviceDir "$scriptDir\rating-service"
Start-Service -serviceName "Trailer Service" -port "5003" -serviceDir "$scriptDir\trailer-service"
Start-Service -serviceName "Frontend Service" -port "5000" -serviceDir "$scriptDir\frontend"

Write-Host ""
Write-Host "All services should be starting..." -ForegroundColor Green
Write-Host ""
Write-Host "Access the application at: http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Services:" -ForegroundColor Yellow
Write-Host "- Movie Service: http://localhost:5001" -ForegroundColor Yellow
Write-Host "- Rating Service: http://localhost:5002" -ForegroundColor Yellow
Write-Host "- Trailer Service: http://localhost:5003" -ForegroundColor Yellow
Write-Host "- Frontend: http://localhost:5000" -ForegroundColor Yellow
Write-Host ""
