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
    ${function:Move-SkillDirectory} = $RealMove
    Test-Case 'Every resource limit accepts the boundary and rejects one byte or entry over' {
        $Package = Join-Path $Temp 'limits.skill'
        New-Package $Package @{ 'SKILL.md' = '#1234567'; 'extra.txt' = '12345678' }
        $ArchiveLength = (Get-Item $Package).Length
        foreach ($Case in @(
            @{ Name = 'MaxArchiveBytes'; Value = $ArchiveLength },
            @{ Name = 'MaxEntries'; Value = 2 },
            @{ Name = 'MaxEntryBytes'; Value = 8 },
            @{ Name = 'MaxExpandedBytes'; Value = 16 },
            @{ Name = 'MaxSourceBytes'; Value = 8 }
        )) {
            $SkillsRoot = Join-Path $Temp ('limit-' + $Case.Name)
            [IO.Directory]::CreateDirectory((Join-Path $SkillsRoot 'user')) | Out-Null
            $Limits = Get-SkillResourceLimits
            $Limits[$Case.Name] = $Case.Value
            Install-SkillFile -SkillFile $Package -Limits $Limits
            $Installed = Join-Path $SkillsRoot 'user/limits/SKILL.md'
            [IO.File]::WriteAllText($Installed, '# original')
            $Limits[$Case.Name] = $Case.Value - 1
            $Caught = $false
            try { Install-SkillFile -SkillFile $Package -Limits $Limits } catch { $Caught = $true }
            Assert-True $Caught "Over-limit package accepted: $($Case.Name)"
            Assert-True ([IO.File]::ReadAllText($Installed) -eq '# original') 'Old installation changed after limit rejection.'
            Assert-NoTransactions $SkillsRoot
        }
        $null = Invoke-Installer @('-SourcePath', $Temp, '-SkillName', 'limits', '-SkillsRoot', (Join-Path $Temp 'cli-limits'), '-MaxEntries', '1') 1
        $null = Invoke-Installer @('-SourcePath', $Temp, '-SkillName', 'limits', '-SkillsRoot', (Join-Path $Temp 'cli-invalid'), '-MaxSourceBytes', '0') 1
        $null = Invoke-Installer @('-SourcePath', $Temp, '-SkillName', 'limits', '-SkillsRoot', (Join-Path $Temp 'cli-exact'), '-MaxEntries', '2', '-MaxSourceBytes', '8')
    }
    Test-Case 'Streaming quotas reject actual expanded bytes before writing beyond limits' {
        foreach ($Case in @(
            @{ Length = 8; EntryLimit = 8; TotalLimit = 8; Initial = 0; Fails = $false },
            @{ Length = 9; EntryLimit = 8; TotalLimit = 100; Initial = 0; Fails = $true },
            @{ Length = 9; EntryLimit = 100; TotalLimit = 16; Initial = 8; Fails = $true },
            @{ Length = 65537; EntryLimit = 65536; TotalLimit = 100000; Initial = 0; Fails = $true }
        )) {
            $InputStream = [IO.MemoryStream]::new((New-Object byte[] $Case.Length))
            $OutputStream = [IO.MemoryStream]::new()
            [long]$Total = $Case.Initial
            $Caught = $false
            try {
                try { $null = Copy-BoundedSkillEntry $InputStream $OutputStream $Case.EntryLimit $Case.TotalLimit ([ref]$Total) } catch { $Caught = $true }
                Assert-True ($Caught -eq $Case.Fails) 'Incorrect streaming quota result.'
                Assert-True ($OutputStream.Length -le $Case.EntryLimit -and $Total -le $Case.TotalLimit) 'Wrote beyond a streaming quota.'
            } finally { $InputStream.Dispose(); $OutputStream.Dispose() }
        }
    }
    Test-Case 'Forged counts, lengths, ZIP64 and malformed directory metadata cannot bypass limits' {
        $Original = Join-Path $Temp 'metadata-original.skill'
        New-Package $Original @{ 'SKILL.md' = '#1234567'; 'extra.txt' = '12345678'; 'empty/' = '' }
        $Bytes = [IO.File]::ReadAllBytes($Original)
        $End = $Bytes.Length - 22
        $Directory = [int][BitConverter]::ToUInt32($Bytes, $End + 16)
        foreach ($Mutation in @('count', 'count-mismatch', 'zip64-count', 'zip64-size', 'split', 'truncated', 'underreported', 'comment-signature')) {
            $Changed = [byte[]]$Bytes.Clone()
            switch ($Mutation) {
                { $_ -in @('count', 'count-mismatch') } { [BitConverter]::GetBytes([uint16]1).CopyTo($Changed, $End + 8); [BitConverter]::GetBytes([uint16]1).CopyTo($Changed, $End + 10) }
                'zip64-count' { [BitConverter]::GetBytes([uint16]65535).CopyTo($Changed, $End + 8); [BitConverter]::GetBytes([uint16]65535).CopyTo($Changed, $End + 10) }
                'zip64-size' { [BitConverter]::GetBytes([uint32]::MaxValue).CopyTo($Changed, $Directory + 24) }
                'split' { [BitConverter]::GetBytes([uint16]1).CopyTo($Changed, $End + 4) }
                'truncated' { [BitConverter]::GetBytes([uint16]65535).CopyTo($Changed, $Directory + 28) }
                'underreported' {
                    $Position = $Directory
                    while ($Position -lt $End) {
                        [BitConverter]::GetBytes([uint32]0).CopyTo($Changed, $Position + 24)
                        $Position += 46 + [BitConverter]::ToUInt16($Bytes, $Position + 28) + [BitConverter]::ToUInt16($Bytes, $Position + 30) + [BitConverter]::ToUInt16($Bytes, $Position + 32)
                    }
                }
                'comment-signature' {
                    [BitConverter]::GetBytes([uint16]4).CopyTo($Changed, $End + 20)
                    $Changed = [byte[]]($Changed + [BitConverter]::GetBytes([uint32]0x06054b50))
                }
            }
            $Package = Join-Path $Temp "$Mutation.skill"
            [IO.File]::WriteAllBytes($Package, $Changed)
            $SkillsRoot = Join-Path $Temp "metadata-$Mutation"
            $Installed = Join-Path $SkillsRoot "user/$Mutation/SKILL.md"
            [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($Installed)) | Out-Null
            [IO.File]::WriteAllText($Installed, '# original')
            $Limits = Get-SkillResourceLimits
            if ($Mutation -eq 'count') { $Limits.MaxEntries = 2 }
            if ($Mutation -eq 'underreported') { $Limits.MaxExpandedBytes = 4 }
            $Caught = $false
            try { Install-SkillFile -SkillFile $Package -Limits $Limits } catch { $Caught = $true }
            Assert-True $Caught "Malformed metadata accepted: $Mutation"
            Assert-True ([IO.File]::ReadAllText($Installed) -eq '# original') 'Metadata failure damaged installed skill.'
            Assert-NoTransactions $SkillsRoot
        }
        # Directory entries consume the same quota as files, even with zero payload.
        $Stream = [IO.File]::OpenRead($Original)
        $Limits = Get-SkillResourceLimits; $Limits.MaxEntries = 2
        $Caught = $false
        try { try { Assert-BoundedZipDirectory $Stream $Limits } catch { $Caught = $true } } finally { $Stream.Dispose() }
        Assert-True $Caught 'Directory entries bypassed the entry quota.'
    }
    Test-Case 'Ordinary ZIP comments remain supported' {
        $Package = Join-Path $Temp 'comment.skill'
        New-Package $Package @{ 'SKILL.md' = '# source' }
        $Bytes = [IO.File]::ReadAllBytes($Package)
        $Comment = [Text.Encoding]::UTF8.GetBytes('normal comment')
        [BitConverter]::GetBytes([uint16]$Comment.Length).CopyTo($Bytes, $Bytes.Length - 2)
        [IO.File]::WriteAllBytes($Package, [byte[]]($Bytes + $Comment))
        $SkillsRoot = Join-Path $Temp 'comment-library'
        [IO.Directory]::CreateDirectory((Join-Path $SkillsRoot 'user')) | Out-Null
        Install-SkillFile -SkillFile $Package
        Assert-True (Test-Path (Join-Path $SkillsRoot 'user/comment/SKILL.md')) 'Normal ZIP comment was rejected.'
        Assert-NoTransactions $SkillsRoot
    }
    Test-Case 'Bounded source scanning preserves BOM and whitespace semantics' {
        $Source = Join-Path $Temp 'bounded-source.md'
        foreach ($Encoding in @([Text.UTF8Encoding]::new($true), [Text.Encoding]::Unicode, [Text.Encoding]::UTF32)) {
            foreach ($Text in @('', " `t`r`n", '# source')) {
                [IO.File]::WriteAllText($Source, $Text, $Encoding)
                $Limit = [Math]::Max(1, (Get-Item $Source).Length)
                Assert-True ((Test-BoundedSkillSource $Source $Limit) -eq ($Text -eq '# source')) 'Source encoding or whitespace behavior changed.'
            }
        }
        [IO.File]::WriteAllText($Source, '# oversized source')
        $Caught = $false
        try { $null = Test-BoundedSkillSource $Source 1 } catch { $Caught = $true }
        Assert-True $Caught 'Immediate non-whitespace bypassed source size limit.'
    }
    Test-Case 'Resource rejection preserves partial batch success and cleans transactions' {
        $Source = Join-Path $Temp 'limited-batch'
        New-Package (Join-Path $Source 'bad.skill') @{ 'SKILL.md' = '# too large' }
        New-Package (Join-Path $Source 'good.skill') @{ 'SKILL.md' = '#' }
        $Root = Join-Path $Temp 'limited-batch-library'
        $null = Invoke-Installer @('-SourcePath', $Source, '-SkillsRoot', $Root, '-MaxSourceBytes', '1') 1
        Assert-True (Test-Path (Join-Path $Root 'user/good/SKILL.md')) 'Valid package in batch was not installed.'
        Assert-True (-not (Test-Path (Join-Path $Root 'user/bad'))) 'Rejected package destination remains.'
        Assert-NoTransactions $Root
    }
    Write-Host "All $Passed installer regression tests passed."
} finally {
    if ($RealMove) { ${function:Move-SkillDirectory} = $RealMove }
    Remove-Item -LiteralPath $Temp -Recurse -Force
}

# Expected failing child processes must not leak their exit code to a calling CI shell.
$global:LASTEXITCODE = 0
