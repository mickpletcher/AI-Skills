<# Exact-case required files; every immediate directory is a candidate. #>
param(
    [string]$Root = (Get-Location).Path,
    [switch]$FailOnIssues,
    [switch]$RepairHints,
    [string]$Python = 'python'
)
$Tool = Join-Path $PSScriptRoot '../../tools/skill_repository.py'
if ($RepairHints) {
    Write-Output 'Required spelling is SKILL.md. For a case-only rename use an intermediate git mv filename.'
}
try {
    & $Python $Tool folders --root $Root
    if ($LASTEXITCODE -ne 0) { exit 1 }
} catch {
    Write-Error "Validation could not run. Install Python 3.11+ and requirements-dev.txt. $_"
    exit 1
}
exit 0
