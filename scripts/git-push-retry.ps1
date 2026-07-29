#!/usr/bin/env pwsh
# Auto-retry git push for connection reset issues
param(
    [int]$MaxRetries = 8,
    [int]$DelaySec = 10
)

for ($i = 1; $i -le $MaxRetries; $i++) {
    Write-Host "[$i/$MaxRetries] Pushing..." -ForegroundColor Cyan
    $output = git push 2>&1
    $output | Out-Host
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Push succeeded!" -ForegroundColor Green
        exit 0
    }
    if ($i -lt $MaxRetries) {
        Write-Host "Failed, retrying in $DelaySec seconds..." -ForegroundColor Yellow
        Start-Sleep -Seconds $DelaySec
    }
}
Write-Host "All retries failed" -ForegroundColor Red
exit 1
