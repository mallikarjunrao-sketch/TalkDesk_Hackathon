# run.ps1 - PULSE Backend Runner Script
param(
    [string]$HostAddress = "127.0.0.1",
    [int]$Port = 8000,
    [switch]$NoReload = $false
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Starting PULSE Backend (Milestone B1)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Ensure project root is in PYTHONPATH
$env:PYTHONPATH = "$PSScriptRoot"

# Activate virtual environment if present
$venvPath = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (Test-Path $venvPath) {
    Write-Host "Using virtual environment: .venv" -ForegroundColor Green
    $pythonExe = $venvPath
} else {
    Write-Host "Virtual environment .venv not found. Using system python." -ForegroundColor Yellow
    $pythonExe = "python"
}

$reloadArg = if ($NoReload) { @() } else { @("--reload") }

Write-Host "Serving on http://${HostAddress}:${Port}" -ForegroundColor Green
Write-Host "Health endpoint: http://${HostAddress}:${Port}/health" -ForegroundColor Green
Write-Host "Interactive docs: http://${HostAddress}:${Port}/docs" -ForegroundColor Green

& $pythonExe -m uvicorn backend.app.main:app --host $HostAddress --port $Port @reloadArg

