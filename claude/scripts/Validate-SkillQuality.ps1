param(
    [string]$Root = (Get-Location).Path,
    [switch]$FailOnIssues
)

$rootPath = (Resolve-Path -LiteralPath $Root).Path
$pathTrimChars = [char[]]@('\', '/')

$platforms = @(
    [pscustomobject]@{ Name = 'Claude'; Path = 'claude/skills'; Source = 'SKILL.md'; Package = $true },
    [pscustomobject]@{ Name = 'ChatGPT'; Path = 'chatgpt/skills'; Source = 'instructions.md'; Package = $false },
    [pscustomobject]@{ Name = 'Copilot'; Path = 'copilot/skills'; Source = 'instructions.md'; Package = $false },
    [pscustomobject]@{ Name = 'Cursor'; Path = 'cursor/skills'; Source = 'instructions.md'; Package = $false },
    [pscustomobject]@{ Name = 'Gemini'; Path = 'gemini/skills'; Source = 'instructions.md'; Package = $false },
    [pscustomobject]@{ Name = 'Perplexity'; Path = 'perplexity/skills'; Source = 'SKILL.md'; Package = $false }
)

$sectionRules = @(
    [pscustomobject]@{ Name = 'Intent'; Pattern = '(?im)^##\s+(Intent|Purpose|Overview|What This Skill Does|Role)\b' },
    [pscustomobject]@{ Name = 'Use When'; Pattern = '(?im)^##\s+(Use When|Trigger When|When To Use|Primary Triggers|Trigger)\b' },
    [pscustomobject]@{ Name = 'Do Not Use When'; Pattern = '(?im)^##\s+(Do Not Use When|Do Not Use|When Not To Use|Out Of Scope)\b' },
    [pscustomobject]@{ Name = 'Workflow'; Pattern = '(?im)^##\s+(Workflow|Process|Operating Procedure|Step-by-Step Workflow|Invention Intake Workflow)\b' },
    [pscustomobject]@{ Name = 'Constraints'; Pattern = '(?im)^##\s+(Constraints|Rules|Safety Rules|Safety|Guardrails|Required Safety Rules|Hard Constraints)\b' },
    [pscustomobject]@{ Name = 'Help And Examples'; Pattern = '(?im)^##\s+(Help And Examples|Help Response|Help|Examples|Example Prompts)\b' },
    [pscustomobject]@{ Name = 'Validation Checklist'; Pattern = '(?im)^##\s+(Validation Checklist|Validation|Test Cases|Quality Checklist|Quality Checks|Testing)\b' }
)

$issues = @()
$checked = 0

foreach ($platform in $platforms) {
    $skillRoot = Join-Path $rootPath $platform.Path
    if (-not (Test-Path -LiteralPath $skillRoot)) {
        continue
    }

    foreach ($dir in Get-ChildItem -LiteralPath $skillRoot -Directory) {
        $sourcePath = Join-Path $dir.FullName $platform.Source
        if (-not (Test-Path -LiteralPath $sourcePath)) {
            continue
        }

        $checked++
        $content = Get-Content -Raw -LiteralPath $sourcePath

        foreach ($rule in $sectionRules) {
            if ($content -notmatch $rule.Pattern) {
                $issues += [pscustomobject]@{
                    Platform = $platform.Name
                    Skill = $dir.Name
                    Issue = "Missing section: $($rule.Name)"
                    File = $sourcePath.Substring($rootPath.Length).TrimStart($pathTrimChars)
                }
            }
        }

        if ($platform.Package) {
            $packagePath = Join-Path $dir.FullName "$($dir.Name).skill"
            if (Test-Path -LiteralPath $packagePath) {
                $sourceItem = Get-Item -LiteralPath $sourcePath
                $packageItem = Get-Item -LiteralPath $packagePath
                if ($packageItem.LastWriteTime -lt $sourceItem.LastWriteTime) {
                    $issues += [pscustomobject]@{
                        Platform = $platform.Name
                        Skill = $dir.Name
                        Issue = 'Package older than source'
                        File = $packagePath.Substring($rootPath.Length).TrimStart($pathTrimChars)
                    }
                }
            }
        }
    }
}

if ($issues.Count -eq 0) {
    Write-Output "Skill quality validation passed."
    Write-Output "Checked skills: $checked"
    exit 0
}

Write-Output "Skill quality validation failed."
Write-Output "Checked skills: $checked"
Write-Output "Issues found: $($issues.Count)"
$issues | Sort-Object Platform, Skill, Issue | Format-Table -AutoSize | Out-String | Write-Output

if ($FailOnIssues) {
    exit 1
}

exit 0
