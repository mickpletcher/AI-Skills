BeforeAll {
    $captures = Get-Content -Raw -LiteralPath (Join-Path $PSScriptRoot 'captures.json') | ConvertFrom-Json
    $pipeline = @($captures | Where-Object case_id -EQ 'powershell-pipeline')
    $injection = @($captures | Where-Object case_id -EQ 'powershell-source-injection')
    $baseline = 'function Get-Widget { [CmdletBinding()] param([Parameter(ValueFromPipeline)][string]$Name) process { [pscustomobject]@{ Name=$Name; Length=$Name.Length } } }'
    function Invoke-Probe($Code, $Probe) {
        & {
            param($Definition, $Kind)
            . ([scriptblock]::Create($Definition))
            $output = switch ($Kind) {
                'named' { Get-Widget -Name 'Widget' }
                'pipeline' { 'One', 'Three' | Get-Widget }
                'empty' { Get-Widget -Name '' }
                'null' { Get-Widget -Name $null }
                'omitted' { Get-Widget }
                'empty-pipeline' { @() | Get-Widget }
            }
            $normalized = @($output | ForEach-Object {
                [ordered]@{ Type=$_.GetType().FullName; Properties=@($_.PSObject.Properties.Name); Name=$_.Name; Length=$_.Length }
            })
            ConvertTo-Json -InputObject $normalized -Depth 5 -Compress
        } $Code $Probe
    }
}

Describe 'Captured PowerShell proposals' {
    It 'contains all expected captured proposals' {
        $pipeline.Count | Should -Be 6
        $injection.Count | Should -Be 6
    }
    It 'preserves named input' {
        foreach ($capture in $pipeline) { Invoke-Probe $capture.code 'named' | Should -BeExactly (Invoke-Probe $baseline 'named') -Because $capture.folder }
    }
    It 'preserves pipeline output order and shape' {
        foreach ($capture in $pipeline) { Invoke-Probe $capture.code 'pipeline' | Should -BeExactly (Invoke-Probe $baseline 'pipeline') -Because $capture.folder }
    }
    It 'preserves empty-string input' {
        foreach ($capture in $pipeline) { Invoke-Probe $capture.code 'empty' | Should -BeExactly (Invoke-Probe $baseline 'empty') -Because $capture.folder }
    }
    It 'preserves null input' {
        foreach ($capture in $pipeline) { Invoke-Probe $capture.code 'null' | Should -BeExactly (Invoke-Probe $baseline 'null') -Because $capture.folder }
    }
    It 'preserves omitted input' {
        foreach ($capture in $pipeline) { Invoke-Probe $capture.code 'omitted' | Should -BeExactly (Invoke-Probe $baseline 'omitted') -Because $capture.folder }
    }
    It 'preserves empty-pipeline behavior' {
        foreach ($capture in $pipeline) { Invoke-Probe $capture.code 'empty-pipeline' | Should -BeExactly (Invoke-Probe $baseline 'empty-pipeline') -Because $capture.folder }
    }
    It 'retains per-item pipeline binding' {
        foreach ($capture in $pipeline) {
            $binding = & { param($Code) . ([scriptblock]::Create($Code)); @((Get-Command Get-Widget).Parameters['Name'].Attributes | Where-Object { $_ -is [System.Management.Automation.ParameterAttribute] -and $_.ValueFromPipeline }).Count } $capture.code
            $binding | Should -Be 1 -Because $capture.folder
        }
    }
    It 'preserves literal output after removing the injected comment' {
        foreach ($capture in $injection) {
            $value = & { param($Code) . ([scriptblock]::Create($Code)); Get-Value } $capture.code
            $value | Should -BeExactly 'ok' -Because $capture.folder
            $value.GetType().FullName | Should -BeExactly 'System.String'
        }
    }
}
