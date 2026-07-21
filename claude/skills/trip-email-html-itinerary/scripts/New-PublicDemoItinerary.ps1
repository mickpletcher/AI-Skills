param(
    [string]$OutputPath = (Join-Path (Get-Location) 'trip-email-html-itinerary-public-demo.html')
)

$templatePath = Join-Path $PSScriptRoot '..\assets\itinerary-template.html'
$template = Get-Content -Raw -LiteralPath $templatePath

$values = @{
    ACTION_COUNT = '1'
    AIRLINE = 'Example Air (Fictional)'
    BOOKING_DETAILS = 'Fictional reservation used only to demonstrate layout'
    BOOKING_NAME = 'Example Air Flight'
    BOOKING_REFERENCE = 'DEMO-BOOKING'
    BOOKING_SUBLABEL = 'Public demonstration record'
    CARD_ISSUER = 'Example Bank (Fictional)'
    CARD_ISSUER_COLLECT_PHONE = 'Not included in public demo'
    CARD_LAST_FOUR = 'DEMO'
    COMPLETED_FLIGHT_ITEM = 'Example outbound flight selected'
    COMPLETED_HOTEL_ITEM = 'Example hotel selected'
    COMPLETED_TOUR_ITEM = 'Example activity selected'
    CONFIRMATION_CODE = 'DEMO123'
    COUNTRY_1 = 'Northstar Republic (Fictional)'
    COUNTRY_2 = 'Solara (Fictional)'
    COUNTRY_COUNT = '2 fictional'
    CRITICAL_ACTION_DETAILS = 'Verify all real details before creating a personal itinerary.'
    CRITICAL_ACTION_TITLE = 'Demo data only'
    DATE_RANGE = 'Sample dates only'
    DAY_1_CONFIRMED_ANCHOR = '09:00 — Fictional harbor walking tour'
    DAY_1_COUNTRY = 'Northstar Republic'
    DAY_1_DATE = 'Day 1'
    DAY_1_FIRST_DROP = 'Example sunset viewpoint'
    DAY_1_NOTE = 'All names, locations, schedules, and reservations are fictional.'
    DAY_1_OPTIONAL_RESTAURANT_OR_ACTIVITY = 'Example local market'
    DAY_1_PACING_CLASS = 'badge-confirmed'
    DAY_1_PACING = 'BALANCED'
    DAY_1_PLANNED_ITEM = '12:30 — Fictional local-specialty lunch'
    DAY_1_SCHEDULE_WARNING = 'No conflicts in this fictional schedule.'
    DAY_1_WEEKDAY = 'SAMPLE'
    DAY_COUNT = '5 fictional'
    DESTINATION_1 = 'Aurora Bay'
    DESTINATION_1_DATES = 'Sample Days 1–3'
    DESTINATION_1_HOTEL = 'Harbor Light Hotel (Fictional)'
    DESTINATION_1_HOTEL_DETAILS = 'Two fictional nights near the demonstration waterfront'
    DESTINATION_1_HOTEL_NOTE = 'No reservation exists. This property is fictional.'
    DESTINATION_1_HOTEL_REFERENCE = 'DEMO-HOTEL'
    DESTINATION_1_NIGHTS = '2'
    DESTINATION_1_TIP = 'Use this area to demonstrate destination-specific advice.'
    DESTINATION_1_TIP_TITLE = 'Public demo tip'
    DESTINATION_1_TRANSPORT_DETAILS = 'Fictional shuttle between the sample terminal and hotel'
    DESTINATION_1_TRANSPORT_NOTE = 'No service is booked or operating.'
    DESTINATION_1_TRANSPORT_TITLE = 'Example Airport Shuttle'
    DESTINATION_2 = 'Lumen Coast'
    DESTINATION_2_DATES = 'Sample Days 3–5'
    DESTINATION_2_HOTEL = 'Sunline Inn (Fictional)'
    DESTINATION_2_NIGHTS = '2'
    DESTINATION_CODE = 'DMO'
    DRIVERS_LICENSE_ISSUER = 'Example Licensing Authority'
    DRIVERS_LICENSE_MASKED = 'DEMO'
    EMERGENCY_CONTACTS = 'Personal contacts are intentionally excluded from the public demo.'
    ENTRY_DETAILS = 'Demonstration text only. Verify current official requirements for a real trip.'
    ENTRY_TITLE = 'Example Entry Checklist'
    FLIGHT_DATE = 'Sample Day 1'
    FLIGHT_DETAILS = 'Example Air · Fictional flight · Economy'
    FLIGHT_TIMES = '08:00 → 10:00 sample time'
    HOTELS_CONFIRMED = '2 fictional'
    HOTELS_TOTAL = '2 fictional'
    MONTH_YEAR = 'Public Demo'
    NEAREST_EMBASSY_CONTACT = 'Not applicable to fictional destinations'
    OPEN_DINING_ITEM = 'Select a real restaurant when building a personal itinerary'
    OPEN_FLIGHT_ITEM = 'Replace fictional segments with verified bookings'
    ORIGIN_CODE = 'SMP'
    PASSID_MASKED = 'DEMO'
    PRIMARY_DESTINATION = 'Public Demo'
    ROUTE = 'SMP → DMO → SMP · Fictional route'
    SECONDARY_DESTINATION = 'Fictional Journey'
    SECURE_PASSPORT_COPY_LOCATION = 'Separate locked note; no ID image is included'
    SELECTED_HOTEL_ITEM = 'Example second hotel under review'
    SNAPSHOT_DATE_TIME = 'Demo generation time'
    TODAY_DATE_AND_LOCATION = 'Next fictional travel day · Aurora Bay'
    TODAY_FIXED_SCHEDULE = '08:00 sample departure · 10:00 sample arrival · 15:00 fictional check-in'
    TODAY_LODGING_OR_TRANSPORT_DETAILS = 'Example shuttle and fictional hotel check-in'
    TODAY_LODGING_OR_TRANSPORT_NOTE = 'Demonstration only. No service exists.'
    TODAY_LODGING_OR_TRANSPORT_TITLE = 'Sample Arrival Plan'
    TODAY_OR_NEXT_LABEL = 'NEXT TRAVEL DAY'
    TODAY_REFERENCE_TITLE = 'Demo references'
    TODAY_SAFE_REFERENCES = 'Flight DEMO123 · Hotel DEMO-HOTEL'
    TODAY_TIMING_NOTE = 'Times are fictional and are not valid for travel.'
    TODAY_WARNING_DETAILS = 'Do not use any demo item as a reservation or travel instruction.'
    TODAY_WARNING_TITLE = 'Fictional data'
    TRAVEL_1_BUFFER = '30-minute sample'
    TRAVEL_1_DESTINATION = 'Harbor Light Hotel'
    TRAVEL_1_DURATION = '25 minutes'
    TRAVEL_1_MODE = 'fictional shuttle'
    TRAVEL_1_ORIGIN = 'Demo Terminal'
    TRAVELER_NAMES = 'Alex Traveler (Fictional)'
    TRIP_TITLE = 'PUBLIC DEMO — Coastal Discovery'
    UPDATED_DATE = 'Public demo build'
    VERIFY_ACTION_DETAILS = 'The finished public example must retain every demo warning.'
    VERIFY_ACTION_TITLE = 'Keep sample labels visible'
}

function Get-DemoValue([string]$Name) {
    if ($values.ContainsKey($Name)) { return $values[$Name] }
    if ($Name -like '*_APPLE_MAPS_URL') { return 'https://maps.apple.com/?q=100+Example+Street+Aurora+Bay' }
    if ($Name -like '*_GOOGLE_MAPS_URL') { return 'https://www.google.com/maps/search/?api=1&query=100+Example+Street+Aurora+Bay' }
    if ($Name -like '*_SOURCE_URL' -or $Name -like '*_REPLACEMENT_URL' -or $Name -like '*_LOST_CARD_URL') { return 'https://example.com/public-demo' }
    if ($Name -like '*_URGENCY_CLASS') { return 'badge-verify' }
    if ($Name -like '*_URGENCY') { return 'VERIFY BEFORE VISITING' }
    if ($Name -like '*_ADDRESS') { return '100 Example Street, Aurora Bay, Northstar Republic (Fictional)' }
    if ($Name -like 'RESTAURANT_*_NAME') { return 'Example Restaurant (Fictional)' }
    if ($Name -like 'RESTAURANT_*_CUISINE') { return 'Demonstration cuisine' }
    if ($Name -like 'RESTAURANT_*_AREA') { return 'Sample district' }
    if ($Name -like 'RESTAURANT_*_PRICE') { return '$$ demo' }
    if ($Name -like 'RESTAURANT_*_WINDOW') { return 'Sample meal window' }
    if ($Name -like 'RESTAURANT_*_FIT') { return 'Shows how a recommendation reason appears' }
    if ($Name -like 'RESTAURANT_*_GUIDANCE') { return 'No reservation exists' }
    if ($Name -like 'ACTIVITY_*_NAME') { return 'Example Activity (Fictional)' }
    if ($Name -like 'ACTIVITY_*_TYPE') { return 'Demonstration activity' }
    if ($Name -like 'ACTIVITY_*_AREA') { return 'Sample district' }
    if ($Name -like 'ACTIVITY_*_DURATION') { return '2-hour sample' }
    if ($Name -like 'ACTIVITY_*_WINDOW') { return 'Sample morning window' }
    if ($Name -like 'ACTIVITY_*_FIT') { return 'Shows how activity fit appears' }
    if ($Name -like 'ACTIVITY_*_GUIDANCE') { return 'No ticket exists' }
    if ($Name -like 'ACTIVITY_*_WEATHER_NOTE') { return 'Fictional weather note' }
    return 'Public demo value'
}

$html = [regex]::Replace($template, '\{\{([A-Z0-9_]+)\}\}', { param($match) Get-DemoValue $match.Groups[1].Value })
$demoCss = '.demo-banner{background:#ffd54f;color:#111;text-align:center;padding:12px 16px;font-family:DM Mono,monospace;font-size:15px;font-weight:700;letter-spacing:1px;border-bottom:3px solid #111}'
$html = $html.Replace('</style>', "$demoCss`r`n</style>")
$banner = '<div class="demo-banner" role="note">PUBLIC DEMO · FICTIONAL DATA · NOT VALID FOR TRAVEL OR BOOKING</div>'
$html = $html.Replace('<body>', "<body>`r`n$banner")
$html = $html.Replace('</footer>', ' · PUBLIC DEMO · FICTIONAL DATA · NOT VALID FOR TRAVEL OR BOOKING</footer>')

$parent = Split-Path -Parent $OutputPath
if ($parent -and -not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
[IO.File]::WriteAllText($OutputPath, $html, [Text.UTF8Encoding]::new($false))
Write-Output (Resolve-Path -LiteralPath $OutputPath).Path
