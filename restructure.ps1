# ==============================================================================
# AquaGuard AI: Windows PowerShell Day-Wise Restructuring Script
# Candidate: Rajana Durga Pavan Kumar (Group C1, TIH IIT Guwahati)
# Target Repo: RajanaDurgaPavanKumar_C1_ONLINETIHIITG
# ==============================================================================
$ErrorActionPreference = "Stop"

Write-Host "Starting repository migration to Day_X_Task_Y structure..." -ForegroundColor Cyan

$pythonExe = "python"
if (Test-Path ".venv\Scripts\python.exe") {
    $pythonExe = ".venv\Scripts\python.exe"
}

& $pythonExe scripts\restructure_repo.py
& $pythonExe scripts\generate_task_readmes.py

Write-Host "Validating git status..." -ForegroundColor Green
git status -s

Write-Host "Restructuring completed successfully!" -ForegroundColor Green
