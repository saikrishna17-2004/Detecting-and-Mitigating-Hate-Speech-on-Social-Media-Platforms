# Reload lexicon on running backend
# Usage: .\scripts\reload_lexicon.ps1 [<path>]
param(
    [string]$Path = 'data/hate_keywords.txt'
)

$body = @{ path = $Path } | ConvertTo-Json
try {
    $res = Invoke-RestMethod -Method Post -Uri 'http://localhost:5000/api/admin/lexicon/reload' -ContentType 'application/json' -Body $body
    $res | ConvertTo-Json -Depth 4
} catch {
    Write-Host "Failed to reload lexicon: $_"
}
