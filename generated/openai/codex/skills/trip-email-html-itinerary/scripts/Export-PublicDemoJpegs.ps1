param(
    [Parameter(Mandatory)]
    [string]$HtmlPath,

    [Parameter(Mandatory)]
    [string]$OutputDirectory,

    [string]$BrowserChannel = 'msedge',

    [ValidateRange(640, 2160)]
    [int]$Width = 1080,

    [ValidateRange(640, 2160)]
    [int]$Height = 1350
)

if ($PSVersionTable.PSEdition -eq 'Core' -and -not $IsWindows) {
    throw 'Public demo JPEG export requires Windows, npx.cmd and System.Drawing. No output was created.'
}

$resolvedHtml = (Resolve-Path -LiteralPath $HtmlPath).Path
$validator = Join-Path $PSScriptRoot 'Test-ItineraryHtml.ps1'
$pwsh = (Get-Command pwsh -ErrorAction Stop).Source
$npx = (Get-Command npx.cmd -ErrorAction Stop).Source

& $pwsh -NoProfile -File $validator -Path $resolvedHtml -PublicDemo -FailOnWarnings
if ($LASTEXITCODE -ne 0) { throw 'Public demo validation failed. JPG export stopped.' }

if (-not (Test-Path -LiteralPath $OutputDirectory)) {
    New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
}
$resolvedOutput = (Resolve-Path -LiteralPath $OutputDirectory).Path

$slides = @(
    [pscustomobject]@{ File = '01-cover.jpg'; Fragment = '' },
    [pscustomobject]@{ File = '02-trip-overview.jpg'; Fragment = 'main-content' },
    [pscustomobject]@{ File = '03-flights.jpg'; Fragment = 'flights' },
    [pscustomobject]@{ File = '04-hotels-and-transport.jpg'; Fragment = 'destinations' },
    [pscustomobject]@{ File = '05-restaurants.jpg'; Fragment = 'restaurants' },
    [pscustomobject]@{ File = '06-activities.jpg'; Fragment = 'activities' },
    [pscustomobject]@{ File = '07-day-plan.jpg'; Fragment = 'day-plan' },
    [pscustomobject]@{ File = '08-bookings.jpg'; Fragment = 'bookings' },
    [pscustomobject]@{ File = '09-travel-admin.jpg'; Fragment = 'admin' },
    [pscustomobject]@{ File = '10-emergency-replacement.jpg'; Fragment = 'emergency-replacement' }
)

$html = Get-Content -Raw -LiteralPath $resolvedHtml
foreach ($slide in $slides) {
    $existingPath = Join-Path $resolvedOutput $slide.File
    if (Test-Path -LiteralPath $existingPath) {
        throw "Output already exists; choose an empty destination: $existingPath"
    }
}
$baseUrl = ([uri]$resolvedHtml).AbsoluteUri.Replace('&', '%26')

foreach ($slide in $slides) {
    if ($slide.Fragment -and $html -notmatch "id=[`"']$([regex]::Escape($slide.Fragment))[`"']") {
        throw "Missing slide target: #$($slide.Fragment)"
    }

    $url = if ($slide.Fragment) { "$baseUrl#$($slide.Fragment)" } else { $baseUrl }
    $outputPath = Join-Path $resolvedOutput $slide.File

    & $npx --yes --package playwright playwright screenshot `
        --channel $BrowserChannel `
        --viewport-size "$Width,$Height" `
        --wait-for-timeout 750 `
        $url `
        $outputPath

    if ($LASTEXITCODE -ne 0) { throw "Screenshot failed: $($slide.File)" }
    $bytes = [IO.File]::ReadAllBytes($outputPath)
    if ($bytes.Length -lt 10000 -or $bytes[0] -ne 0xFF -or $bytes[1] -ne 0xD8) {
        throw "Invalid JPEG output: $($slide.File)"
    }

    Add-Type -AssemblyName System.Drawing
    $image = [Drawing.Image]::FromFile($outputPath)
    try {
        if ($image.Width -ne $Width -or $image.Height -ne $Height) {
            throw "Unexpected dimensions for $($slide.File): $($image.Width)x$($image.Height)"
        }
    }
    finally {
        $image.Dispose()
    }
}

Get-ChildItem -LiteralPath $resolvedOutput -Filter '*.jpg' | Sort-Object Name | Select-Object -ExpandProperty FullName
