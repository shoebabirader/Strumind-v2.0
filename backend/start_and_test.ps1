# StruMind Backend Startup and Test Script
# This script starts the backend server and runs comprehensive tests

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  STRUMIND BACKEND STARTUP & TEST" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check if database exists
if (Test-Path "strumind.db") {
    Write-Host "✓ Database found" -ForegroundColor Green
} else {
    Write-Host "⚠ Database not found - creating..." -ForegroundColor Yellow
    python setup_database.py
}

# Start backend server in background
Write-Host "`n→ Starting backend server..." -ForegroundColor Cyan
$backend = Start-Process python -ArgumentList "main.py" -PassThru -NoNewWindow

# Wait a bit for server to start
Write-Host "→ Waiting for server to initialize..." -ForegroundColor Cyan
Start-Sleep -Seconds 5

# Run tests
Write-Host "`n→ Running comprehensive tests...`n" -ForegroundColor Cyan
python test_complete_app.py

# Store exit code
$testExitCode = $LASTEXITCODE

# Stop backend server
Write-Host "`n→ Stopping backend server..." -ForegroundColor Cyan
Stop-Process -Id $backend.Id -Force

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  TEST COMPLETE" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

exit $testExitCode
