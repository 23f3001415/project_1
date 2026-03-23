$tokenPath = Join-Path $PSScriptRoot "final_token.txt"
$token = Get-Content -Raw $tokenPath
$token = $token.Trim()
Set-Clipboard -Value $token
Write-Output "Copied q11 token to clipboard."
