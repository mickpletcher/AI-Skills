<#
.SYNOPSIS
    Installs, updates, removes, and lists Claude skill files for Claude Desktop.

.DESCRIPTION
    Manages the Claude Skills library at the configured SkillsRoot path.
    Scans a source directory for .skill files and installs them into the
    user skills directory. Supports selective install, update-only mode,
    removal of individual skills, and listing all currently installed skills.

    Source priority:
      1. -SourcePath if specified
      2. -RepoPath\skills if a cloned repo is provided
      3. $env:USERPROFILE\Downloads (default)

.PARAMETER SkillsRoot
    Root path for the Claude Skills library.
    Defaults to $env:USERPROFILE\OneDrive\Documents\Claude\Skills.

.PARAMETER SourcePath
    Path to scan for .skill files.
    Defaults to the user's Downloads folder.

.PARAMETER RepoPath
    Path to a cloned copy of the mickpletcher/Anthropic repo.
    If provided, installs .skill files found under RepoPath\skills\.

.PARAMETER SkillName
    Install or remove a single named skill only.
    Name must match the skill filename without extension (e.g. 'powershell-automation').

.PARAMETER Remove
    Remove the specified skill. Requires -SkillName.

.PARAMETER UpdateOnly
    Only install skills that are already installed. Skips new skills.

.PARAMETER List
    Display all currently installed skills and exit.

.PARAMETER WhatIf
    Show what would be installed or removed without making any changes.

.EXAMPLE
    powershell.exe -ExecutionPolicy Bypass -File Initialize-ClaudeSkills.ps1

.EXAMPLE
    powershell.exe -ExecutionPolicy Bypass -File Initialize-ClaudeSkills.ps1 -SkillName "powershell-automation"

.EXAMPLE
    powershell.exe -ExecutionPolicy Bypass -File Initialize-ClaudeSkills.ps1 -Remove -SkillName "blog-post"

.EXAMPLE
    powershell.exe -ExecutionPolicy Bypass -File Initialize-ClaudeSkills.ps1 -UpdateOnly

.EXAMPLE
    powershell.exe -ExecutionPolicy Bypass -File Initialize-ClaudeSkills.ps1 -RepoPath "C:\Repos\Anthropic"

.EXAMPLE
    powershell.exe -ExecutionPolicy Bypass -File Initialize-ClaudeSkills.ps1 -List

.NOTES
    ===========================================================================
    Created on:     2026-03-27
    Created by:     Mick Pletcher
    Organization:   CBIZ
    Filename:       Initialize-ClaudeSkills.ps1
    ===========================================================================
#>

[CmdletBinding(SupportsShouldProcess)]
param (
    [Parameter(Mandatory = $false)]
    [ValidateNotNullOrEmpty()]
    [string]$SkillsRoot = "$env:USERPROFILE\OneDrive\Documents\Claude\Skills",

    [Parameter(Mandatory = $false)]
    [ValidateNotNullOrEmpty()]
    [string]$SourcePath = "$env:USERPROFILE\Downloads",

    [Parameter(Mandatory = $false)]
    [string]$RepoPath = '',

    [Parameter(Mandatory = $false)]
    [string]$SkillName = '',

    [Parameter(Mandatory = $false)]
    [switch]$Remove,

    [Parameter(Mandatory = $false)]
    [switch]$UpdateOnly,

    [Parameter(Mandatory = $false)]
    [switch]$List
)

#region Functions

function Write-Log {
<#
.SYNOPSIS
    Writes a color-coded message to the console.

.PARAMETER Message
    The message to display.

.PARAMETER Severity
    1 = Information (white), 2 = Warning (yellow), 3 = Error (red).
#>
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [string]$Message,

        [Parameter(Mandatory = $false)]
        [ValidateRange(1, 3)]
        [int]$Severity = 1
    )

    $Colors = @{ 1 = 'White'; 2 = 'Yellow'; 3 = 'Red' }
    $Prefix = @{ 1 = '[INFO] '; 2 = '[WARN] '; 3 = '[ERROR]' }
    Write-Host "$($Prefix[$Severity]) $Message" -ForegroundColor $Colors[$Severity]
}

function Initialize-SkillsDirectory {
<#
.SYNOPSIS
    Creates the Claude Skills folder structure if it does not already exist.
#>
    [CmdletBinding()]
    param ()

    $Folders = @(
        $SkillsRoot,
        "$SkillsRoot\user",
        "$SkillsRoot\public"
    )

    foreach ($Folder in $Folders) {
        if (-not (Test-Path -Path $Folder)) {
            try {
                if ($PSCmdlet.ShouldProcess($Folder, 'Create directory')) {
                    New-Item -Path $Folder -ItemType Directory -Force | Out-Null
                    Write-Log -Message "Created: $Folder"
                }
            } catch {
                Write-Log -Message "Failed to create '$Folder': $_" -Severity 3
                exit 1
            }
        }
    }
}

function Get-InstalledSkills {
<#
.SYNOPSIS
    Returns a list of currently installed skill directory names.
#>
    [CmdletBinding()]
    param ()

    $UserSkillsPath = "$SkillsRoot\user"
    if (-not (Test-Path -Path $UserSkillsPath)) {
        return @()
    }
    return Get-ChildItem -Path $UserSkillsPath -Directory |
        Select-Object -ExpandProperty Name
}

function Show-InstalledSkills {
<#
.SYNOPSIS
    Displays all currently installed skills to the console.
#>
    [CmdletBinding()]
    param ()

    $Installed = Get-InstalledSkills

    Write-Host ""
    Write-Host "Installed Skills ($($Installed.Count))" -ForegroundColor Cyan
    Write-Host "================================" -ForegroundColor Cyan

    if ($Installed.Count -eq 0) {
        Write-Log -Message "No skills currently installed at: $SkillsRoot\user" -Severity 2
    } else {
        foreach ($Skill in ($Installed | Sort-Object)) {
            Write-Host "  $Skill" -ForegroundColor Green
        }
    }
    Write-Host ""
}

function Get-SkillFiles {
<#
.SYNOPSIS
    Returns .skill files found in the resolved source path.

.PARAMETER Path
    Directory to scan for .skill files.
#>
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if (-not (Test-Path -Path $Path)) {
        Write-Log -Message "Source path not found: $Path" -Severity 3
        return @()
    }

    try {
        $Files = Get-ChildItem -Path $Path -Filter '*.skill' -File -ErrorAction Stop

        if ($SkillName -ne '') {
            $Files = $Files | Where-Object { $_.BaseName -eq $SkillName }
        }

        return $Files
    } catch {
        Write-Log -Message "Failed to scan '$Path': $_" -Severity 3
        return @()
    }
}

function Install-SkillFile {
<#
.SYNOPSIS
    Extracts a .skill file into the Claude Skills user directory.

.PARAMETER SkillFile
    Full path to the .skill file to install.
#>
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [ValidateScript({ Test-Path $_ -PathType Leaf })]
        [string]$SkillFile
    )

    $Name        = [System.IO.Path]::GetFileNameWithoutExtension($SkillFile)
    $Destination = "$SkillsRoot\user\$Name"
    $IsUpdate    = Test-Path -Path $Destination

    if ($UpdateOnly -and -not $IsUpdate) {
        Write-Log -Message "Skipped (not installed): $Name" -Severity 2
        return
    }

    $Action = if ($IsUpdate) { 'Update' } else { 'Install' }

    if ($PSCmdlet.ShouldProcess($Name, $Action)) {
        if ($IsUpdate) {
            try {
                Remove-Item -Path $Destination -Recurse -Force -ErrorAction Stop
            } catch {
                Write-Log -Message "Failed to remove existing '$Name' before update: $_" -Severity 2
            }
        }

        try {
            Expand-Archive -Path $SkillFile -DestinationPath $Destination -Force -ErrorAction Stop
            $Tag   = if ($IsUpdate) { '[UPDATED]' } else { '[NEW]    ' }
            $Color = if ($IsUpdate) { 'Cyan' } else { 'Green' }
            Write-Host "  $Tag $Name" -ForegroundColor $Color
        } catch {
            Write-Log -Message "Failed to extract '$Name': $_" -Severity 3
        }
    }
}

function Remove-Skill {
<#
.SYNOPSIS
    Removes a single installed skill by name.

.PARAMETER Name
    The skill directory name to remove.
#>
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true)]
        [string]$Name
    )

    $Target = "$SkillsRoot\user\$Name"

    if (-not (Test-Path -Path $Target)) {
        Write-Log -Message "Skill not found: $Name" -Severity 2
        return
    }

    if ($PSCmdlet.ShouldProcess($Name, 'Remove skill')) {
        try {
            Remove-Item -Path $Target -Recurse -Force -ErrorAction Stop
            Write-Log -Message "Removed: $Name"
        } catch {
            Write-Log -Message "Failed to remove '$Name': $_" -Severity 3
        }
    }
}

#endregion Functions

#region Main

Write-Host ""
Write-Host "Claude Skills Manager" -ForegroundColor Cyan
Write-Host "=====================" -ForegroundColor Cyan
Write-Host ""

# List mode
if ($List) {
    Show-InstalledSkills
    exit 0
}

# Remove mode
if ($Remove) {
    if ($SkillName -eq '') {
        Write-Log -Message "-SkillName is required when using -Remove." -Severity 3
        exit 1
    }
    Write-Log -Message "Removing skill: $SkillName"
    Initialize-SkillsDirectory
    Remove-Skill -Name $SkillName
    Write-Host ""
    Write-Log -Message "Done. Restart Claude Desktop to apply changes."
    exit 0
}

# Resolve source path
$ResolvedSource = $SourcePath

if ($RepoPath -ne '') {
    $RepoSkillsPath = Join-Path $RepoPath 'skills'
    if (Test-Path -Path $RepoSkillsPath) {
        $ResolvedSource = $RepoSkillsPath
        Write-Log -Message "Using repo source: $ResolvedSource"
    } else {
        Write-Log -Message "Repo skills folder not found at: $RepoSkillsPath" -Severity 2
        Write-Log -Message "Falling back to: $SourcePath"
    }
}

# Ensure directory structure exists
Initialize-SkillsDirectory

# Find skill files
$SkillFiles = Get-SkillFiles -Path $ResolvedSource

if ($SkillFiles.Count -eq 0) {
    if ($SkillName -ne '') {
        Write-Log -Message "No .skill file found matching '$SkillName' in: $ResolvedSource" -Severity 2
    } else {
        Write-Log -Message "No .skill files found in: $ResolvedSource" -Severity 2
        Write-Host ""
        Write-Host "  Download .skill files to: $ResolvedSource" -ForegroundColor Yellow
        Write-Host "  Or use -RepoPath:          -RepoPath 'C:\Repos\Anthropic'" -ForegroundColor Yellow
    }
    Write-Host ""
    exit 0
}

# Install
$ModeLabel = if ($UpdateOnly) { ' (update only)' } else { '' }
Write-Log -Message "Processing $($SkillFiles.Count) skill file(s)$ModeLabel"
Write-Host ""

foreach ($File in $SkillFiles) {
    Install-SkillFile -SkillFile $File.FullName
}

# Final summary
Write-Host ""
Write-Host "=====================" -ForegroundColor Cyan
Write-Host ""
Write-Host "All installed skills:" -ForegroundColor Cyan
foreach ($Skill in (Get-InstalledSkills | Sort-Object)) {
    Write-Host "  $Skill" -ForegroundColor Green
}

Write-Host ""
Write-Log -Message "Done. Restart Claude Desktop to load updated skills."

#endregion Main
