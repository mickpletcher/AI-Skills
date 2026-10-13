<#
Run with PowerShell 7+ or Windows PowerShell 5.1. No Pester dependency.
All writes are confined to a unique temporary directory, removed on completion.
#>
$ErrorActionPreference = 'Stop'
$Installer = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../Initialize-ClaudeSkills.ps1'))
$Repo = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../..'))
$Engine = (Get-Process -Id $PID).Path
$Temp = Join-Path ([IO.Path]::GetTempPath()) ('skill-installer-tests-' + [guid]::NewGuid().ToString('N'))
[IO.Directory]::CreateDirectory($Temp) | Out-Null
$Passed = 0

function Assert-True($Condition, [string]$Message) {
    if (-not $Condition) { throw $Message }
}
function New-Package([string]$Path, [hashtable]$Entries) {
    [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($Path)) | Out-Null
    $Zip = [IO.Compression.ZipFile]::Open($Path, [IO.Compression.ZipArchiveMode]::Create)
    try {
        foreach ($Name in $Entries.Keys) {
            $Entry = $Zip.CreateEntry($Name)
            $Writer = [IO.StreamWriter]::new($Entry.Open())
            try { $Writer.Write($Entries[$Name]) } finally { $Writer.Dispose() }
        }
    } finally { $Zip.Dispose() }
}
function Invoke-Installer([string[]]$Arguments, [int]$ExpectedExit = 0) {
    $Output = & $Engine -NoProfile -File $Installer @Arguments 2>&1 | Out-String
    Assert-True ($LASTEXITCODE -eq $ExpectedExit) "Expected exit $ExpectedExit, got $LASTEXITCODE. $Output"
    return $Output
}
function Test-Case([string]$Name, [scriptblock]$Body) {
    & $Body
    $script:Passed++
    Write-Host "PASS: $Name"
}
function Assert-NoTransactions([string]$Root) {
    Assert-True (@(Get-ChildItem -LiteralPath $Root -Filter '.install-*' -Force).Count -eq 0) 'Temporary transaction leaked.'
}

try {
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    # Import function definitions only, so fault injection cannot run the script's main/exit.
    $ParseErrors = $null
    $Ast = [Management.Automation.Language.Parser]::ParseFile($Installer, [ref]$null, [ref]$ParseErrors)
    Assert-True (-not $ParseErrors) "Installer parse errors: $ParseErrors"
    foreach ($Definition in $Ast.EndBlock.Statements | Where-Object { $_ -is [Management.Automation.Language.FunctionDefinitionAst] }) {
        . ([scriptblock]::Create($Definition.Extent.Text))
    }
    $RealMove = ${function:Move-SkillDirectory}
    $UpdateOnly = $false
    $SkillName = ''

    Test-Case 'Actual repository layout discovers all packages, WhatIf writes nothing' {
        $Root = Join-Path $Temp 'actual-library'
        $Expected = @(Get-ChildItem (Join-Path $Repo 'claude/skills') -Recurse -Filter '*.skill').Count
        $Output = Invoke-Installer @('-RepoPath', $Repo, '-SkillsRoot', $Root, '-WhatIf')
        Assert-True ($Expected -gt 0 -and $Output.Contains("Processing $Expected skill file(s)")) $Output
        Assert-True (-not (Test-Path $Root)) 'WhatIf created the library.'
    }
    Test-Case 'Actual repository packages extract and validate into a temporary library' {
        $Root = Join-Path $Temp 'actual-installed-library'
        $null = Invoke-Installer @('-RepoPath', $Repo, '-SkillsRoot', $Root)
        $Packages = @(Get-ChildItem (Join-Path $Repo 'claude/skills') -Recurse -Filter '*.skill')
        foreach ($Package in $Packages) {
            Assert-True (Test-Path (Join-Path $Root "user/$($Package.BaseName)/SKILL.md")) "Missing installed source: $Package"
        }
        Assert-NoTransactions $Root
    }
    Test-Case 'Nested repository discovery installs and safely updates a named skill' {
        $Source = Join-Path $Temp 'repo/claude/skills/example/example.skill'
        $Root = Join-Path $Temp 'library'
        New-Package $Source @{ 'SKILL.md' = '# version one'; 'obsolete.txt' = 'old' }
        $null = Invoke-Installer @('-RepoPath', (Join-Path $Temp 'repo'), '-SkillsRoot', $Root, '-SkillName', 'example')
        Remove-Item $Source
        New-Package $Source @{ 'SKILL.md' = '# version two'; 'docs/new.txt' = 'new' }
        $null = Invoke-Installer @('-RepoPath', (Join-Path $Temp 'repo'), '-SkillsRoot', $Root, '-UpdateOnly')
        Assert-True ([IO.File]::ReadAllText((Join-Path $Root 'user/example/SKILL.md')) -eq '# version two') 'Update not installed.'
        Assert-True (-not (Test-Path (Join-Path $Root 'user/example/obsolete.txt'))) 'Obsolete files retained.'
        Assert-True (Test-Path (Join-Path $Root 'user/example/docs/new.txt')) 'Nested file missing.'
        Assert-NoTransactions $Root
        $null = Invoke-Installer @('-RepoPath', (Join-Path $Temp 'repo'), '-SkillsRoot', $Root, '-WhatIf')
        Assert-True ([IO.File]::ReadAllText((Join-Path $Root 'user/example/SKILL.md')) -eq '# version two') 'WhatIf modified an installed skill.'
        Assert-NoTransactions $Root
    }
    Test-Case 'Legacy repository layout remains supported' {
        $Source = Join-Path $Temp 'legacy/skills/nested/legacy.skill'
        New-Package $Source @{ 'SKILL.md' = '# legacy' }
        $Root = Join-Path $Temp 'legacy-library'
        $null = Invoke-Installer @('-RepoPath', (Join-Path $Temp 'legacy'), '-SkillsRoot', $Root)
        Assert-True (Test-Path (Join-Path $Root 'user/legacy/SKILL.md')) 'Legacy package not installed.'
    }
    Test-Case 'Explicit source wins over repository; recursive scan works' {
        $Source = Join-Path $Temp 'explicit/nested/explicit.skill'
        New-Package $Source @{ 'SKILL.md' = '# explicit' }
        $Root = Join-Path $Temp 'explicit-library'
        $null = Invoke-Installer @('-SourcePath', (Join-Path $Temp 'explicit'), '-RepoPath', (Join-Path $Temp 'missing-repo'), '-SkillsRoot', $Root)
        Assert-True (Test-Path (Join-Path $Root 'user/explicit/SKILL.md')) 'Explicit source not used.'
    }
    Test-Case 'Empty, missing and filtered sources fail before library creation' {
        $Empty = Join-Path $Temp 'empty'
        [IO.Directory]::CreateDirectory($Empty) | Out-Null
        $Root = Join-Path $Temp 'empty-library'
        $Output = Invoke-Installer @('-SourcePath', $Empty, '-SkillsRoot', $Root) 1
        Assert-True ($Output.Contains('No .skill packages')) $Output
        $null = Invoke-Installer @('-SourcePath', (Join-Path $Temp 'absent'), '-SkillsRoot', $Root) 1
        $null = Invoke-Installer @('-RepoPath', $Empty, '-SkillsRoot', $Root) 1
        $null = Invoke-Installer @('-RepoPath', (Join-Path $Temp 'repo'), '-SkillsRoot', $Root, '-SkillName', 'unknown') 1
        Assert-True (-not (Test-Path $Root)) 'Failed discovery created the library.'
    }
    Test-Case 'Duplicate package names fail instead of selecting an arbitrary update' {
        New-Package (Join-Path $Temp 'duplicates/a/example.skill') @{ 'SKILL.md' = '# a' }
        New-Package (Join-Path $Temp 'duplicates/b/example.skill') @{ 'SKILL.md' = '# b' }
        $Output = Invoke-Installer @('-SourcePath', (Join-Path $Temp 'duplicates'), '-SkillsRoot', (Join-Path $Temp 'duplicates-library')) 1
        Assert-True ($Output.Contains('Duplicate skill package names')) $Output
    }
    Test-Case 'UpdateOnly skips new skills without staging' {
        $Root = Join-Path $Temp 'update-only-library'
        $null = Invoke-Installer @('-SourcePath', (Join-Path $Temp 'explicit'), '-SkillsRoot', $Root, '-UpdateOnly')
        Assert-True (-not (Test-Path (Join-Path $Root 'user/explicit'))) 'UpdateOnly installed a new skill.'
        Assert-NoTransactions $Root
    }
    Test-Case 'Malformed, corrupt, empty-source and unsafe archives preserve existing installation' {
        $Root = Join-Path $Temp 'bad-library'
        $Old = Join-Path $Root 'user/example/SKILL.md'
        [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($Old)) | Out-Null
        [IO.File]::WriteAllText($Old, '# original')
        $SourceDir = Join-Path $Temp 'bad-source'
        [IO.Directory]::CreateDirectory($SourceDir) | Out-Null
        $Source = Join-Path $SourceDir 'example.skill'
        New-Package $Source @{ 'SKILL.md' = '# corrupt' }
        $Bytes = [IO.File]::ReadAllBytes($Source)
        [IO.File]::WriteAllBytes($Source, $Bytes[0..([int]($Bytes.Length / 2))])
        $null = Invoke-Installer @('-SourcePath', $SourceDir, '-SkillsRoot', $Root) 1
        Assert-True ([IO.File]::ReadAllText($Old) -eq '# original') 'Truncated ZIP damaged original.'
        Assert-NoTransactions $Root
        Remove-Item $Source
        $Cases = @(
            @{ 'README.md' = 'missing source' },
            @{ 'SKILL.md' = '  ' },
            @{ 'SKILL.md' = '# unsafe'; '../escape.txt' = 'escape' },
            @{ 'SKILL.md' = '# unsafe'; '..\escape.txt' = 'escape' },
            @{ 'SKILL.md' = '# unsafe'; '/absolute.txt' = 'escape' },
            @{ 'SKILL.md' = '# unsafe'; 'C:\absolute.txt' = 'escape' },
            @{ 'SKILL.md' = '# unsafe'; 'file:stream' = 'escape' },
            @{ 'SKILL.md' = '# unsafe'; 'folder./file' = 'escape' },
            @{ 'SKILL.md' = '# unsafe'; 'NUL.txt' = 'escape' }
        )
        foreach ($Entries in $Cases) {
            New-Package $Source $Entries
            $null = Invoke-Installer @('-SourcePath', $SourceDir, '-SkillsRoot', $Root) 1
            Assert-True ([IO.File]::ReadAllText($Old) -eq '# original') 'Old installation changed by invalid archive.'
            Assert-NoTransactions $Root
            Remove-Item $Source
        }
        [IO.File]::WriteAllText($Source, 'not a zip archive')
        $null = Invoke-Installer @('-SourcePath', $SourceDir, '-SkillsRoot', $Root) 1
        Assert-True ([IO.File]::ReadAllText($Old) -eq '# original') 'Corrupt archive replaced old skill.'
        Assert-NoTransactions $Root
        Assert-True (-not (Test-Path (Join-Path $Root 'escape.txt'))) 'Archive escaped staging.'
    }
    Test-Case 'Archive symlinks and case-colliding entries are rejected' {
        foreach ($Kind in @('link', 'duplicate')) {
            $Source = Join-Path $Temp "$Kind-source/example.skill"
            New-Package $Source @{ 'SKILL.md' = '# example' }
            $Zip = [IO.Compression.ZipFile]::Open($Source, [IO.Compression.ZipArchiveMode]::Update)
            try {
                if ($Kind -eq 'link') {
                    $Entry = $Zip.CreateEntry('link')
                    $Entry.ExternalAttributes = -1577058304 # Unix symlink 0120000 in upper bits
                } else {
                    $null = $Zip.CreateEntry('skill.md')
                }
            } finally { $Zip.Dispose() }
            $Root = Join-Path $Temp "$Kind-library"
            $null = Invoke-Installer @('-SourcePath', ([IO.Path]::GetDirectoryName($Source)), '-SkillsRoot', $Root) 1
            Assert-True (-not (Test-Path (Join-Path $Root 'user/example'))) 'Unsafe archive installed.'
            Assert-NoTransactions $Root
        }
    }
    Test-Case 'A failed package returns nonzero while independent successful installs remain' {
        $SourceDir = Join-Path $Temp 'batch'
        New-Package (Join-Path $SourceDir 'good.skill') @{ 'SKILL.md' = '# good' }
        New-Package (Join-Path $SourceDir 'bad.skill') @{ 'README.md' = 'missing source' }
        $Root = Join-Path $Temp 'batch-library [test]'
        $Output = Invoke-Installer @('-SourcePath', $SourceDir, '-SkillsRoot', $Root) 1
        Assert-True ($Output.Contains('1 package(s) failed')) $Output
        Assert-True (Test-Path -LiteralPath (Join-Path $Root 'user/good/SKILL.md')) 'Successful package missing.'
        Assert-True (-not (Test-Path -LiteralPath (Join-Path $Root 'user/bad'))) 'Invalid package installed.'
        Assert-NoTransactions $Root
    }
    Test-Case 'Failed first install leaves no destination or staging' {
        $SkillsRoot = Join-Path $Temp 'new-failure-library'
        [IO.Directory]::CreateDirectory((Join-Path $SkillsRoot 'user')) | Out-Null
        function Move-SkillDirectory($Source, $Destination) { throw 'injected new install failure' }
        $Caught = $false
        try { Install-SkillFile -SkillFile (Join-Path $Temp 'repo/claude/skills/example/example.skill') } catch { $Caught = $true }
        Assert-True $Caught 'New install failure was swallowed.'
        Assert-True (-not (Test-Path (Join-Path $SkillsRoot 'user/example'))) 'Failed install left a destination.'
        Assert-NoTransactions $SkillsRoot
    }
    Test-Case 'Failed replacement rolls back old installation and cleans staging' {
        $SkillsRoot = Join-Path $Temp 'rollback-library'
        $Old = Join-Path $SkillsRoot 'user/example/SKILL.md'
        [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($Old)) | Out-Null
        [IO.File]::WriteAllText($Old, '# original')
        function Move-SkillDirectory($Source, $Destination) {
            if ([IO.Path]::GetFileName($Source) -eq 'staged') { throw 'injected replacement failure' }
            [IO.Directory]::Move($Source, $Destination)
        }
        $Caught = $false
        try { Install-SkillFile -SkillFile (Join-Path $Temp 'repo/claude/skills/example/example.skill') } catch {
            $Caught = $true
            Assert-True ($_.ToString().Contains('previous installation restored')) $_
        }
        Assert-True $Caught 'Replacement failure was swallowed.'
        Assert-True ([IO.File]::ReadAllText($Old) -eq '# original') 'Rollback did not restore original.'
        Assert-NoTransactions $SkillsRoot
    }
    Test-Case 'Failed backup move preserves old installation and cleans staging' {
        $SkillsRoot = Join-Path $Temp 'backup-failure-library'
        $Old = Join-Path $SkillsRoot 'user/example/SKILL.md'
        [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($Old)) | Out-Null
        [IO.File]::WriteAllText($Old, '# original')
        function Move-SkillDirectory($Source, $Destination) { throw 'injected backup move failure' }
        $Caught = $false
        try { Install-SkillFile -SkillFile (Join-Path $Temp 'repo/claude/skills/example/example.skill') } catch { $Caught = $true }
        Assert-True $Caught 'Backup failure was swallowed.'
        Assert-True ([IO.File]::ReadAllText($Old) -eq '# original') 'Backup failure damaged original.'
        Assert-NoTransactions $SkillsRoot
    }
    Test-Case 'Rollback failure retains backup and reports recovery path' {
        $SkillsRoot = Join-Path $Temp 'recovery-library'
        $Old = Join-Path $SkillsRoot 'user/example/SKILL.md'
        [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($Old)) | Out-Null
        [IO.File]::WriteAllText($Old, '# original')
        function Move-SkillDirectory($Source, $Destination) {
            if ([IO.Path]::GetFileName($Source) -in @('staged', 'backup')) { throw 'injected move failure' }
            [IO.Directory]::Move($Source, $Destination)
        }
        $Caught = $false
        try { Install-SkillFile -SkillFile (Join-Path $Temp 'repo/claude/skills/example/example.skill') } catch {
            $Caught = $true
            Assert-True ($_.ToString().Contains('Previous installation retained at')) $_
        }
        Assert-True $Caught 'Rollback failure was swallowed.'
        $Transactions = @(Get-ChildItem -LiteralPath $SkillsRoot -Filter '.install-*' -Force)
        Assert-True ($Transactions.Count -eq 1) 'Recovery directory missing.'
        Assert-True ([IO.File]::ReadAllText((Join-Path $Transactions[0].FullName 'backup/SKILL.md')) -eq '# original') 'Recovery backup damaged.'
    }
    Write-Host "All $Passed installer regression tests passed."
} finally {
    if ($RealMove) { ${function:Move-SkillDirectory} = $RealMove }
    Remove-Item -LiteralPath $Temp -Recurse -Force
}

# Expected failing child processes must not leak their exit code to a calling CI shell.
$global:LASTEXITCODE = 0
