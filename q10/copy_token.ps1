$token = Get-Content -Raw -Path "$PSScriptRoot\final_token.txt"
$token = $token.Trim()
Set-Clipboard -Value $token
Write-Host "Q10 token copied to clipboard."
Write-Host ("Length: " + $token.Length)
Write-Host ("Dot count: " + (($token.ToCharArray() | Where-Object { $_ -eq '.' }).Count))
