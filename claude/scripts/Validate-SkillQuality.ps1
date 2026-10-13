<# Uses the shared offline validator; failures always return nonzero. #>
param(
    [string]$Root = (Get-Location).Path,
    [switch]$FailOnIssues,
    [string]$Python = 'python'
)
$Tool = Join-Path $PSScriptRoot '../../tools/skill_repository.py'
try {
    & $Python $Tool validate --root $Root
    if ($LASTEXITCODE -ne 0) { exit 1 }
} catch {
    Write-Error "Validation could not run. Install Python 3.11+ and requirements-dev.txt. $_"
    exit 1
}
exit 0
