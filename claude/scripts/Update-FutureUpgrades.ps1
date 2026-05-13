[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$SkillsRoot = (Join-Path (Get-Location) 'claude\skills')
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-SkillDirectories {
    param(
        [string]$Path
    )

    Get-ChildItem -LiteralPath $Path -Directory | Where-Object {
        (Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md')) -or
        (Test-Path -LiteralPath (Join-Path $_.FullName 'README.md'))
    } | Sort-Object Name
}

function Get-RecentCompletedWork {
    param(
        [string]$UpgradePath
    )

    if (-not (Test-Path -LiteralPath $UpgradePath)) {
        return @('- No applied upgrades recorded yet.')
    }

    $lines = Get-Content -LiteralPath $UpgradePath
    $items = New-Object System.Collections.Generic.List[string]

    foreach ($line in $lines) {
        if ($line -match '^\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$') {
            $date = $matches[1].Trim()
            $upgrade = $matches[2].Trim()
            $notes = $matches[3].Trim()
            $items.Add("- ${date}: $upgrade. $notes")
        }
    }

    if ($items.Count -eq 0) {
        return @('- No applied upgrades recorded yet.')
    }

    return $items
}

function Get-PreservedTierContent {
    param(
        [string]$FuturePath
    )

    $result = @{
        '## Tier 1: High Value' = @()
        '## Tier 2: Medium Value' = @()
        '## Tier 3: Long Term' = @()
    }

    if (-not (Test-Path -LiteralPath $FuturePath)) {
        return $result
    }

    $currentSection = ''
    foreach ($line in Get-Content -LiteralPath $FuturePath) {
        if ($result.ContainsKey($line.Trim())) {
            $currentSection = $line.Trim()
            continue
        }

        if ($line -match '^## ') {
            $currentSection = ''
            continue
        }

        if ([string]::IsNullOrEmpty($currentSection)) {
            continue
        }

        $result[$currentSection] += $line
    }

    return $result
}

function Get-TierBody {
    param(
        [string[]]$Lines,
        [string]$Placeholder
    )

    $content = ($Lines -join [Environment]::NewLine).Trim()
    if ([string]::IsNullOrWhiteSpace($content)) {
        return "- $Placeholder"
    }

    return $content
}

function New-FutureUpgradesContent {
    param(
        [string]$SkillName,
        [string[]]$CompletedWork,
        [hashtable]$PreservedContent
    )

    $today = Get-Date -Format 'yyyy-MM-dd'
    $recentBlock = ($CompletedWork -join [Environment]::NewLine).Trim()
    $tier1 = Get-TierBody -Lines $PreservedContent['## Tier 1: High Value'] -Placeholder 'Add the next high value upgrade here'
    $tier2 = Get-TierBody -Lines $PreservedContent['## Tier 2: Medium Value'] -Placeholder 'Add the next medium effort upgrade here'
    $tier3 = Get-TierBody -Lines $PreservedContent['## Tier 3: Long Term'] -Placeholder 'Add the next long term upgrade here'

    @"
# Future Upgrades: $SkillName

This file is local planning for future work.

Last auto update: $today

## Recent Completed Work

$recentBlock

## Tier 1: High Value

$tier1

## Tier 2: Medium Value

$tier2

## Tier 3: Long Term

$tier3
"@.Trim() + [Environment]::NewLine
}

$resolvedSkillsRoot = (Resolve-Path -LiteralPath $SkillsRoot).Path
$skillDirectories = Get-SkillDirectories -Path $resolvedSkillsRoot
$updatedCount = 0

foreach ($directory in $skillDirectories) {
    $futurePath = Join-Path $directory.FullName 'future-upgrades.md'
    $upgradePath = Join-Path $directory.FullName 'upgrades.md'
    $completedWork = Get-RecentCompletedWork -UpgradePath $upgradePath
    $preservedContent = Get-PreservedTierContent -FuturePath $futurePath
    $newContent = New-FutureUpgradesContent -SkillName $directory.Name -CompletedWork $completedWork -PreservedContent $preservedContent
    $currentContent = if (Test-Path -LiteralPath $futurePath) { Get-Content -LiteralPath $futurePath -Raw } else { '' }

    if ($currentContent -ceq $newContent) {
        continue
    }

    if ($PSCmdlet.ShouldProcess($futurePath, 'Update future upgrades file')) {
        Set-Content -LiteralPath $futurePath -Value $newContent -Encoding utf8
        $updatedCount++
    }
}

Write-Host "Processed skill folders: $($skillDirectories.Count)"
Write-Host "Updated future-upgrades files: $updatedCount"
