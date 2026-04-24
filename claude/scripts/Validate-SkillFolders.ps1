param(
    [string]$Root = (Get-Location).Path,
    [switch]$FailOnIssues,
    [switch]$RepairHints
)

$rootPath = (Resolve-Path -LiteralPath $Root).Path
$requiredFiles = @('README.md', 'skill.md')

function Get-RenameSuggestion {
    param(
        [string]$FolderPath,
        [string]$MissingName,
        [string]$RepoRoot
    )

    $variants = @()

    switch ($MissingName) {
        'README.md' { $variants = @('Readme.md', 'readme.md') }
        'skill.md' { $variants = @('SKILL.md', 'Skill.md') }
        default { $variants = @() }
    }

    foreach ($variant in $variants) {
        $variantPath = Join-Path $FolderPath $variant
        if (Test-Path -LiteralPath $variantPath) {
            $src = $variantPath.Substring($RepoRoot.Length).TrimStart('\\', '/')
            $dst = (Join-Path $FolderPath $MissingName).Substring($RepoRoot.Length).TrimStart('\\', '/')
            return "git mv `"$src`" `"$dst`""
        }
    }

    return ''
}

$candidateDirs = Get-ChildItem -LiteralPath $rootPath -Directory | Where-Object {
    (Test-Path -LiteralPath (Join-Path $_.FullName 'skill.md')) -or
    (Test-Path -LiteralPath (Join-Path $_.FullName 'skill.zip'))
}

$issues = @()

foreach ($dir in $candidateDirs) {
    foreach ($required in $requiredFiles) {
        $filePath = Join-Path $dir.FullName $required
        if (-not (Test-Path -LiteralPath $filePath)) {
            $suggestion = ''
            if ($RepairHints) {
                $suggestion = Get-RenameSuggestion -FolderPath $dir.FullName -MissingName $required -RepoRoot $rootPath
            }

            $issues += [pscustomobject]@{
                Folder = $dir.Name
                Missing = $required
                Suggestion = $suggestion
            }
        }
    }
}

if ($issues.Count -eq 0) {
    Write-Host "Skill folder validation passed."
    Write-Host "Checked folders: $($candidateDirs.Count)"
    exit 0
}

Write-Host "Skill folder validation failed."
Write-Host "Checked folders: $($candidateDirs.Count)"
Write-Host "Issues found: $($issues.Count)"
$issues | Sort-Object Folder, Missing | Format-Table -AutoSize | Out-String | Write-Host

if ($RepairHints) {
    $commands = $issues | Where-Object { -not [string]::IsNullOrWhiteSpace($_.Suggestion) } | Select-Object -ExpandProperty Suggestion -Unique
    if ($commands.Count -gt 0) {
        Write-Host "Repair hints:"
        $commands | ForEach-Object { Write-Host $_ }
    }
}

if ($FailOnIssues) {
    exit 1
}

exit 0
