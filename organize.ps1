# ==============================================================================
# organize.ps1: Windows PowerShell script to consolidate folders into Day_Wise_Tasks/
# Candidate: Rajana Durga Pavan Kumar (Group C1, TIH IIT Guwahati)
# ==============================================================================
$ErrorActionPreference = "Stop"

$targetDir = "Day_Wise_Tasks"
if (!(Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir | Out-Null
}

Write-Host "Consolidating day folders into $targetDir/..." -ForegroundColor Cyan

$folders = Get-ChildItem -Directory -Filter "Day_*_Task_*" | Where-Object { $_.Name -ne $targetDir }

foreach ($f in $folders) {
    $dest = Join-Path $targetDir $f.Name
    if (Test-Path $dest) {
        Write-Host "Skipping (already exists): $($f.Name)" -ForegroundColor Yellow
    } else {
        Write-Host "Moving $($f.Name) -> $dest" -ForegroundColor Green
        git mv $f.FullName $dest
    }
}

$count = (Get-ChildItem -Directory -Path $targetDir -Filter "Day_*_Task_*").Count
Write-Host "Total task folders in $targetDir: $count" -ForegroundColor Cyan

$missing = @()
for ($day = 1; $day -le 28; $day++) {
    for ($task = 1; $task -le 2; $task++) {
        $expected = Join-Path $targetDir "Day_${day}_Task_${task}"
        if (!(Test-Path $expected)) {
            $missing += $expected
        }
    }
}

if ($missing.Count -eq 0) {
    Write-Host "SUCCESS: All 56 Day_X_Task_Y folders across Days 1 to 28 are verified present." -ForegroundColor Green
} else {
    Write-Host "WARNING: $($missing.Count) folders are missing." -ForegroundColor Red
}

Write-Host "Repository structure at level 2:" -ForegroundColor Cyan
Get-ChildItem -Directory | Select-Object Name
