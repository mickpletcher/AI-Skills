[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$TaskName = 'Resume Writer Weekly Tips Refresh',
    [ValidateSet('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')]
    [string]$DayOfWeek = 'Monday',
    [ValidatePattern('^\d{2}:\d{2}$')]
    [string]$StartTime = '09:00',
    [string]$SkillRoot
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($SkillRoot)) {
    $scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
    $SkillRoot = Split-Path -Parent $scriptDirectory
}

$refreshScriptPath = Join-Path $SkillRoot 'scripts\Invoke-ResumeTipsRefresh.ps1'

if (-not (Test-Path -LiteralPath $refreshScriptPath)) {
    throw "Refresh script not found: $refreshScriptPath"
}

$startBoundary = [datetime]::ParseExact($StartTime, 'HH:mm', $null)
if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    throw "Scheduled task already exists; preserve it and choose a different task name: $TaskName"
}
$action = New-ScheduledTaskAction `
    -Execute 'powershell.exe' `
    -Argument ('-ExecutionPolicy Bypass -File "{0}"' -f $refreshScriptPath) `
    -WorkingDirectory $SkillRoot

$trigger = New-ScheduledTaskTrigger `
    -Weekly `
    -DaysOfWeek $DayOfWeek `
    -At $startBoundary

$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -MultipleInstances IgnoreNew

if ($PSCmdlet.ShouldProcess($TaskName, 'Register weekly resume tips task')) {
Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description 'Creates the weekly resume-writer tips review packet.' | Out-Null
}

[pscustomobject]@{
    TaskName = $TaskName
    DayOfWeek = $DayOfWeek
    StartTime = $StartTime
    SkillRoot = $SkillRoot
    RefreshScript = $refreshScriptPath
}
