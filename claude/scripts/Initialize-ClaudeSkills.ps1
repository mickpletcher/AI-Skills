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
      2. -RepoPath\claude\skills (or legacy RepoPath\skills)
      3. $env:USERPROFILE\Downloads (default)

.PARAMETER SkillsRoot
    Root path for the Claude Skills library.
    Defaults to $env:USERPROFILE\OneDrive\Documents\Claude\Skills.

.PARAMETER SourcePath
    Path to scan recursively for .skill files.
    Defaults to the user's Downloads folder.

.PARAMETER RepoPath
    Path to a cloned copy of AI-Skills. Scans RepoPath\claude\skills\
    recursively, with RepoPath\skills\ supported for legacy layouts.
    An explicit SourcePath takes precedence. Invalid repositories do not fall back to Downloads.

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
    powershell.exe -ExecutionPolicy Bypass -File Initialize-ClaudeSkills.ps1 -RepoPath "C:\Repos\AI-Skills"

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
    [ValidatePattern('^$|^[a-zA-Z0-9][a-zA-Z0-9_-]*$')]
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
    [CmdletBinding(SupportsShouldProcess)]
    param ()

    $Folders = @(
        $SkillsRoot,
        "$SkillsRoot\user",
        "$SkillsRoot\public"
    )

    foreach ($Folder in $Folders) {
        if (-not (Test-Path -LiteralPath $Folder)) {
            try {
                if ($PSCmdlet.ShouldProcess($Folder, 'Create directory')) {
                    New-Item -Path $Folder -ItemType Directory -Force -ErrorAction Stop | Out-Null
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
    if (-not (Test-Path -LiteralPath $UserSkillsPath)) {
        return @()
    }
    return Get-ChildItem -LiteralPath $UserSkillsPath -Directory |
        Select-Object -ExpandProperty Name
}

function Show-InstalledSkills {
<#
.SYNOPSIS
    Displays all currently installed skills to the console.
#>
    [CmdletBinding()]
    param ()

    $Installed = @(Get-InstalledSkills)

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

    if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
        throw "Source directory not found: $Path"
    }

    $Files = @(Get-ChildItem -LiteralPath $Path -Filter '*.skill' -File -Recurse -ErrorAction Stop |
        Where-Object { $SkillName -eq '' -or $_.BaseName -eq $SkillName } |
        Sort-Object FullName)
    if ($Files.Count -eq 0) {
        throw "No .skill packages found in '$Path' matching skill '$SkillName'."
    }
    $Duplicates = @($Files | Group-Object BaseName | Where-Object Count -gt 1)
    if ($Duplicates.Count -gt 0) {
        throw "Duplicate skill package names in '$Path': $($Duplicates.Name -join ', '). Select an unambiguous source."
    }
    return $Files
}

function Assert-SafeDirectory {
    param ([string]$Path)

    # Reject links within the configured library, including the library itself.
    $Current = [IO.Path]::GetFullPath($Path)
    $Boundary = [IO.Path]::GetFullPath($SkillsRoot).TrimEnd([IO.Path]::DirectorySeparatorChar)
    while ($Current) {
        if (Test-Path -LiteralPath $Current) {
            $Item = Get-Item -LiteralPath $Current -Force -ErrorAction Stop
            if (-not $Item.PSIsContainer -or ($Item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
                throw "Installation path must be a real directory, not a file or link: $Current"
            }
        }
        if ($Current.TrimEnd([IO.Path]::DirectorySeparatorChar) -eq $Boundary) { break }
        $Current = [IO.Path]::GetDirectoryName($Current)
    }
}

function Expand-ValidatedSkill {
    param ([string]$SkillFile, [string]$Destination)

    Add-Type -AssemblyName System.IO.Compression.FileSystem -ErrorAction Stop
    $Archive = [IO.Compression.ZipFile]::OpenRead($SkillFile)
    try {
        $Paths = @{}
        $Prefix = [IO.Path]::GetFullPath($Destination) + [IO.Path]::DirectorySeparatorChar
        foreach ($Entry in $Archive.Entries) {
            # Treat both separators as separators on every host, including Unix.
            $Relative = $Entry.FullName.Replace('\', '/')
            $Parts = $Relative.TrimEnd('/').Split('/')
            if ([string]::IsNullOrWhiteSpace($Relative) -or $Relative.StartsWith('/') -or
                ($Parts | Where-Object {
                    $_ -eq '' -or $_ -eq '.' -or $_ -eq '..' -or
                    $_ -match '[<>:"|?*\x00-\x1f]' -or $_ -match '[. ]$' -or
                    $_ -match '^(?i:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)'
                })) {
                throw "Unsafe archive path '$($Entry.FullName)' in '$SkillFile'."
            }
            $UnixType = ($Entry.ExternalAttributes -shr 16) -band 0xF000
            if ($UnixType -notin @(0, 0x8000, 0x4000) -or ($Entry.ExternalAttributes -band 0x400)) {
                throw "Archive links or special files are not allowed: $($Entry.FullName)"
            }
            $Target = [IO.Path]::GetFullPath((Join-Path $Destination ($Parts -join [IO.Path]::DirectorySeparatorChar)))
            if (-not $Target.StartsWith($Prefix, [StringComparison]::OrdinalIgnoreCase) -or $Paths.ContainsKey($Target)) {
                throw "Duplicate or escaping archive path: $($Entry.FullName)"
            }
            $Paths[$Target] = $true
            if ($Relative.EndsWith('/')) {
                [IO.Directory]::CreateDirectory($Target) | Out-Null
            } else {
                [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($Target)) | Out-Null
                $InputStream = $Entry.Open()
                try {
                    $OutputStream = [IO.File]::Open($Target, [IO.FileMode]::CreateNew)
                    try { $InputStream.CopyTo($OutputStream) } finally { $OutputStream.Dispose() }
                } finally { $InputStream.Dispose() }
            }
        }
        $Source = Join-Path $Destination 'SKILL.md'
        if (-not (Test-Path -LiteralPath $Source -PathType Leaf) -or
            [string]::IsNullOrWhiteSpace([IO.File]::ReadAllText($Source))) {
            throw "Package must contain a nonempty SKILL.md at its root: $SkillFile"
        }
    } finally { $Archive.Dispose() }
}

function Move-SkillDirectory {
    param ([string]$Source, [string]$Destination)
    # Same-filesystem directory renames; never merge into or overwrite a directory.
    [IO.Directory]::Move($Source, $Destination)
}

function Install-SkillFile {
    [CmdletBinding(SupportsShouldProcess)]
    param (
        [Parameter(Mandatory = $true)]
        [string]$SkillFile
    )

    $Name = [IO.Path]::GetFileNameWithoutExtension($SkillFile)
    if ($Name -notmatch '^[a-zA-Z0-9][a-zA-Z0-9_-]*$') {
        throw "Unsafe skill package name: $Name"
    }
    $Root = [IO.Path]::GetFullPath($SkillsRoot)
    $Destination = Join-Path (Join-Path $Root 'user') $Name
    Assert-SafeDirectory -Path $Destination
    $IsUpdate = Test-Path -LiteralPath $Destination
    if ($UpdateOnly -and -not $IsUpdate) {
        Write-Log -Message "Skipped (not installed): $Name" -Severity 2
        return
    }
    $Action = if ($IsUpdate) { 'Update' } else { 'Install' }
    if (-not $PSCmdlet.ShouldProcess($Destination, "$Action from $SkillFile")) { return }

    # Keep staging and backup on the destination filesystem, outside the user catalog.
    $Transaction = Join-Path $Root ('.install-' + [guid]::NewGuid().ToString('N'))
    $Stage = Join-Path $Transaction 'staged'
    $Backup = Join-Path $Transaction 'backup'
    $Committed = $false
    try {
        [IO.Directory]::CreateDirectory($Stage) | Out-Null
        Expand-ValidatedSkill -SkillFile $SkillFile -Destination $Stage
        if ($IsUpdate) { Move-SkillDirectory -Source $Destination -Destination $Backup }
        try {
            Move-SkillDirectory -Source $Stage -Destination $Destination
        } catch {
            $ReplacementError = $_
            if (Test-Path -LiteralPath $Backup) {
                try {
                    Move-SkillDirectory -Source $Backup -Destination $Destination
                } catch {
                    throw "Replacement failed for '$Name': $ReplacementError. Rollback also failed: $_. Previous installation retained at '$Backup'; restore it manually after resolving the destination conflict."
                }
                throw "Replacement failed for '$Name'; previous installation restored. $ReplacementError"
            }
            throw "Installation failed for '$Name': $ReplacementError"
        }
        $Committed = $true
        $Tag = if ($IsUpdate) { '[UPDATED]' } else { '[NEW]' }
        Write-Log -Message "$Tag $Name"
    } finally {
        # Never delete the only remaining copy of a previous installation.
        if (-not $Committed -and (Test-Path -LiteralPath $Backup)) {
            Write-Log -Message "Recovery files retained at '$Transaction'." -Severity 3
        } elseif (Test-Path -LiteralPath $Transaction) {
            try {
                Remove-Item -LiteralPath $Transaction -Recurse -Force -ErrorAction Stop
            } catch {
                Write-Log -Message "Could not clean temporary files at '$Transaction': $_" -Severity 2
            }
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

# Resolve relative library paths against the PowerShell location, not the process cwd.
try {
    $SkillsRoot = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($SkillsRoot)
} catch {
    Write-Log -Message "Invalid skills library path: $_" -Severity 3
    exit 1
}

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

# Discover before creating the library. Explicit SourcePath takes precedence.
try {
    $ResolvedSource = $SourcePath
    if (-not $PSBoundParameters.ContainsKey('SourcePath') -and $RepoPath -ne '') {
        $RepoSkillsPath = Join-Path (Join-Path $RepoPath 'claude') 'skills'
        $LegacySkillsPath = Join-Path $RepoPath 'skills'
        if (Test-Path -LiteralPath $RepoSkillsPath -PathType Container) {
            $ResolvedSource = $RepoSkillsPath
        } elseif (Test-Path -LiteralPath $LegacySkillsPath -PathType Container) {
            $ResolvedSource = $LegacySkillsPath
        } else {
            throw "Repository has no claude/skills or skills directory: $RepoPath"
        }
    }
    Write-Log -Message "Using source: $ResolvedSource"
    $SkillFiles = @(Get-SkillFiles -Path $ResolvedSource)
    Assert-SafeDirectory -Path (Join-Path $SkillsRoot 'user')
    Initialize-SkillsDirectory
} catch {
    Write-Log -Message "Cannot prepare installation: $_" -Severity 3
    exit 1
}

# Install
$ModeLabel = if ($UpdateOnly) { ' (update only)' } else { '' }
Write-Log -Message "Processing $($SkillFiles.Count) skill file(s)$ModeLabel"
Write-Host ""

$Failures = 0
foreach ($File in $SkillFiles) {
    try {
        Install-SkillFile -SkillFile $File.FullName
    } catch {
        $Failures++
        Write-Log -Message "Failed package '$($File.FullName)': $_" -Severity 3
    }
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
if ($Failures -gt 0) {
    Write-Log -Message "$Failures package(s) failed. See diagnostics above; successful packages were retained." -Severity 3
    exit 1
}
Write-Log -Message "Done. Restart Claude Desktop to load updated skills."

#endregion Main
