param(
    [Parameter(Mandatory)]
    [string]$Path,

    [string]$EmergencyContactsPath,

    [switch]$PublicDemo,

    [switch]$FailOnWarnings
)

$htmlPath = (Resolve-Path -LiteralPath $Path).Path
$html = Get-Content -Raw -LiteralPath $htmlPath
$errors = [System.Collections.Generic.List[string]]::new()
$warnings = [System.Collections.Generic.List[string]]::new()

function Add-Error([string]$Message) {
    $errors.Add($Message)
}

function Add-Warning([string]$Message) {
    $warnings.Add($Message)
}

if ($html -notmatch '(?is)^\s*<!DOCTYPE html>') { Add-Error 'Missing <!DOCTYPE html>.' }
if ($html -notmatch '(?is)<meta\s+name=["'']viewport["'']') { Add-Error 'Missing viewport meta tag.' }
if ($html -match '\{\{[A-Z0-9_]+\}\}') { Add-Error 'Unresolved template placeholders remain.' }
if ($html -match '(?is)<script\b') { Add-Error 'JavaScript is not allowed.' }
if ($html -match '(?is)<iframe\b') { Add-Error 'Iframes are not allowed.' }
if ($html -match '(?i)javascript\s*:') { Add-Error 'javascript: links are not allowed.' }
if ($html -match '(?i)(file://|[A-Z]:\\Users\\|/Users/|/home/)') { Add-Error 'Local filesystem path found.' }

$requiredText = @(
    'Destination Sequence',
    'Action Items',
    'Flights',
    'Day-by-Day Itinerary',
    'Booking References',
    'Booking Checklist',
    'Travel Admin',
    'Emergency Replacement'
)

foreach ($text in $requiredText) {
    if ($html -notmatch [regex]::Escape($text)) { Add-Error "Missing required section: $text." }
}

$ids = [regex]::Matches($html, '(?i)\bid=["'']([^"'']+)["'']') | ForEach-Object { $_.Groups[1].Value }
$duplicateIds = $ids | Group-Object | Where-Object Count -gt 1
foreach ($duplicate in $duplicateIds) { Add-Error "Duplicate id: $($duplicate.Name)." }

$fragmentLinks = [regex]::Matches($html, '(?i)href=["'']#([^"'']+)["'']') | ForEach-Object { $_.Groups[1].Value }
foreach ($fragment in $fragmentLinks) {
    if (($ids | Where-Object { $_ -eq $fragment }).Count -ne 1) { Add-Error "Broken internal navigation target: #$fragment." }
}

$hrefs = [regex]::Matches($html, '(?i)href=["'']([^"'']+)["'']') | ForEach-Object { $_.Groups[1].Value }
foreach ($href in $hrefs) {
    if ($href.StartsWith('#')) { continue }
    $uri = $null
    if (-not [uri]::TryCreate($href, [UriKind]::Absolute, [ref]$uri) -or $uri.Scheme -notin @('http', 'https', 'mailto', 'tel')) {
        Add-Error "Invalid or unsupported link: $href."
    }
}

$addressBlocks = [regex]::Matches($html, '(?is)<div\s+class=["'']info-card-address["''].*?</div>')
if ($addressBlocks.Count -eq 0) { Add-Error 'No plain-text address blocks found.' }

$appleMapLinks = [regex]::Matches($html, '(?i)href=["'']https://maps\.apple\.com/[^"'']+["'']').Count
$googleMapLinks = [regex]::Matches($html, '(?i)href=["'']https://www\.google\.com/maps/search/[^"'']+["'']').Count
if ($appleMapLinks -lt $addressBlocks.Count) { Add-Warning 'Some addresses do not have Apple Maps links.' }
if ($googleMapLinks -lt $addressBlocks.Count) { Add-Warning 'Some addresses do not have Google Maps links.' }

if ($html -match '(?i)\b(?:PIN|CVV|CVC|password|access\s+code)\b\s*[:#=-]\s*(?!\[redacted\])\S+') {
    Add-Error 'Possible unredacted secret found.'
}

if ($html -match '(?<!\d)(?:\d[ -]*?){13,19}(?!\d)') {
    Add-Error 'Possible full payment-card number found.'
}

if ($html -notmatch '(?is)@media\s*\(max-width:\s*430px\)') { Add-Error 'Missing narrow-phone media query.' }
if ($html -notmatch '(?is)@media\s*\(prefers-reduced-motion:\s*reduce\)') { Add-Error 'Missing reduced-motion accessibility rule.' }
if ($html -notmatch '(?is):focus-visible') { Add-Error 'Missing visible keyboard-focus styling.' }
if ($html -notmatch '(?is)min-height:\s*44px') { Add-Error 'Missing 44px minimum tap target.' }

if ($PublicDemo) {
    foreach ($label in @('PUBLIC DEMO', 'FICTIONAL DATA', 'NOT VALID FOR TRAVEL OR BOOKING')) {
        if ([regex]::Matches($html, [regex]::Escape($label), [Text.RegularExpressions.RegexOptions]::IgnoreCase).Count -lt 2) {
            Add-Error "Public demo label must appear at least twice: $label."
        }
    }

    if ($html -notmatch '(?is)<title>[^<]*PUBLIC DEMO[^<]*</title>') { Add-Error 'Public demo title is not clearly labeled.' }
    if ($html -notmatch '(?is)class=["''][^"'']*demo-watermark[^"'']*["'']') { Add-Error 'Public demo is missing the persistent screenshot watermark.' }
    if ($EmergencyContactsPath) { Add-Error 'Public demos must not include an emergency contacts sheet.' }

    $allowedDemoHosts = @(
        'fonts.googleapis.com',
        'maps.apple.com',
        'www.google.com',
        'example.com',
        'travel.state.gov',
        'www.usembassy.gov',
        'ttp.dhs.gov'
    )

    foreach ($href in $hrefs) {
        if ($href.StartsWith('#')) { continue }
        $uri = [uri]$href
        if ($uri.Host -notin $allowedDemoHosts) { Add-Error "Public demo contains a non-approved external host: $($uri.Host)." }
    }
}

if ($EmergencyContactsPath) {
    $contactsPath = (Resolve-Path -LiteralPath $EmergencyContactsPath).Path
    $contacts = Get-Content -Raw -LiteralPath $contactsPath
    if ($contacts -match '\{\{[A-Z0-9_]+\}\}') { Add-Error 'Emergency contacts sheet has unresolved placeholders.' }
    if ($contacts -match '(?i)\b(?:PIN|CVV|CVC|password|access\s+code)\b\s*[:#=-]\s*(?!\[redacted\])\S+') { Add-Error 'Emergency contacts sheet may contain an unredacted secret.' }
    if ($contacts -match '(?<!\d)(?:\d[ -]*?){13,19}(?!\d)') { Add-Error 'Emergency contacts sheet may contain a full payment-card number.' }
}

foreach ($warning in $warnings) { Write-Warning $warning }
foreach ($errorMessage in $errors) { Write-Error $errorMessage }

Write-Output "Errors: $($errors.Count)"
Write-Output "Warnings: $($warnings.Count)"

if ($errors.Count -gt 0 -or ($FailOnWarnings -and $warnings.Count -gt 0)) { exit 1 }
exit 0
