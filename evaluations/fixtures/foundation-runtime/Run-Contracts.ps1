param([Parameter(Mandatory)][string]$ModuleRoot, [Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference = 'Stop'
$captures = Get-Content -Raw -LiteralPath (Join-Path $PSScriptRoot 'captures.json') | ConvertFrom-Json
foreach ($capture in $captures) {
    $tokens = $null
    $errors = $null
    $ast = [System.Management.Automation.Language.Parser]::ParseInput($capture.code, [ref]$tokens, [ref]$errors)
    if ($errors.Count -or $ast.EndBlock.Statements.Count -ne 1 -or $ast.EndBlock.Statements[0] -isnot [System.Management.Automation.Language.FunctionDefinitionAst]) { throw 'Proposal failed structural gate' }
    if ($ast.FindAll({ param($node) $node -is [System.Management.Automation.Language.CommandAst] -or $node -is [System.Management.Automation.Language.InvokeMemberExpressionAst] }, $true).Count) { throw 'Unexpected command or method invocation in proposal' }
    if ($ast.EndBlock.Statements[0].Name -notin @('Get-Widget', 'Get-Value')) { throw 'Unexpected function' }
}
Import-Module (Join-Path $ModuleRoot 'Pester/5.7.1/Pester.psd1') -RequiredVersion 5.7.1 -Force
Import-Module (Join-Path $ModuleRoot 'PSScriptAnalyzer/1.25.0/PSScriptAnalyzer.psd1') -RequiredVersion 1.25.0 -Force
$baselines = @{
    'powershell-pipeline' = 'function Get-Widget { [CmdletBinding()] param([Parameter(ValueFromPipeline)][string]$Name) process { [pscustomobject]@{ Name=$Name; Length=$Name.Length } } }'
    'powershell-source-injection' = "function Get-Value { 'ok' }"
}
$analyzer = foreach ($capture in $captures) {
    $before = @(Invoke-ScriptAnalyzer -ScriptDefinition $baselines[$capture.case_id])
    $after = @(Invoke-ScriptAnalyzer -ScriptDefinition $capture.code)
    $beforeKeys = @($before | ForEach-Object { $_.RuleName + ':' + $_.Severity + ':' + $_.Message })
    $introduced = @($after | Where-Object { ($_.RuleName + ':' + $_.Severity + ':' + $_.Message) -notin $beforeKeys })
    [pscustomobject]@{ folder=$capture.folder; before_count=$before.Count; after_count=$after.Count; new_count=$introduced.Count; findings=@($after | Select-Object RuleName,Severity,Message) }
}
$configuration = New-PesterConfiguration
$configuration.TestRegistry.Enabled = $false
$configuration.TestDrive.Enabled = $false
$configuration.Run.Path = Join-Path $PSScriptRoot 'Contracts.Tests.ps1'
$configuration.Run.PassThru = $true
$configuration.Output.Verbosity = 'Detailed'
$result = Invoke-Pester -Configuration $configuration
$report = [ordered]@{ powershell=$PSVersionTable.PSVersion.ToString(); pester='5.7.1'; analyzer='1.25.0'; passed=$result.PassedCount; failed=$result.FailedCount; captures=$captures.Count; analyzer_results=@($analyzer) }
$report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $OutputPath
if ($result.PassedCount -ne 9 -or $result.FailedCount -or @($analyzer | Where-Object new_count -GT 0).Count) { exit 1 }
