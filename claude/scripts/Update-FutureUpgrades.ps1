[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$SkillsRoot = (Join-Path (Get-Location) 'claude\skills')
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-SkillDirectories {
    param(
        [string]$Path
    )

    Get-ChildItem -LiteralPath $Path -Directory | Where-Object {
        (Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md')) -or
        (Test-Path -LiteralPath (Join-Path $_.FullName 'README.md'))
    } | Sort-Object Name
}

function Get-RecentCompletedWork {
    param(
        [string]$UpgradePath
    )

    if (-not (Test-Path -LiteralPath $UpgradePath)) {
        return @('- No applied upgrades recorded yet.')
    }

    $lines = Get-Content -LiteralPath $UpgradePath
    $items = New-Object System.Collections.Generic.List[string]

    foreach ($line in $lines) {
        if ($line -match '^\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$') {
            $date = $matches[1].Trim()
            $upgrade = $matches[2].Trim()
            $notes = $matches[3].Trim()
            $items.Add("- ${date}: $upgrade. $notes")
        }
    }

    if ($items.Count -eq 0) {
        return @('- No applied upgrades recorded yet.')
    }

    return $items
}

function Get-PreservedTierContent {
    param(
        [string]$FuturePath
    )

    $result = @{
        '## Tier 1: High Value' = @()
        '## Tier 2: Medium Value' = @()
        '## Tier 3: Long Term' = @()
    }

    if (-not (Test-Path -LiteralPath $FuturePath)) {
        return $result
    }

    $currentSection = ''
    foreach ($line in Get-Content -LiteralPath $FuturePath) {
        if ($result.ContainsKey($line.Trim())) {
            $currentSection = $line.Trim()
            continue
        }

        if ($line -match '^## ') {
            $currentSection = ''
            continue
        }

        if ([string]::IsNullOrEmpty($currentSection)) {
            continue
        }

        $result[$currentSection] += $line
    }

    return $result
}

function Get-TierBody {
    param(
        [string[]]$Lines,
        [string]$Placeholder
    )

    $meaningfulLines = @(
        $Lines | Where-Object {
            $trimmed = $_.Trim()
            if ([string]::IsNullOrWhiteSpace($trimmed)) {
                return $false
            }

            return ($trimmed -notmatch '^- Add the next .+ here$')
        }
    )

    $content = ($meaningfulLines -join [Environment]::NewLine).Trim()
    if ([string]::IsNullOrWhiteSpace($content)) {
        return $Placeholder.Trim()
    }

    return $content
}

function Get-DefaultTierSuggestions {
    param(
        [string]$SkillName
    )

    $map = @{
        'alpaca-trading' = @{
            Tier1 = @(
                '- Add broker capability profiles so the skill can tailor repo advice to Alpaca limitations, paper trading behavior, and deployment safeguards'
                '- Add order lifecycle validation checklists for entries, exits, partial fills, and cancel replace flows before proposing repo changes'
                '- Add a regression test matrix section that maps common trading changes to the exact Python and PowerShell test passes to run'
            )
            Tier2 = @(
                '- Add strategy mode templates for momentum, mean reversion, and bracket order workflows with repo specific implementation prompts'
                '- Add structured risk review output that flags missing guardrails such as max position size, duplicate order prevention, and stale signal handling'
                '- Add broker migration guidance so the skill can compare Alpaca specific code to a more portable execution layer'
            )
            Tier3 = @(
                '- Add a portfolio level architecture mode that designs multi strategy repo layouts with shared execution, data, and risk modules'
                '- Add historical incident review prompts that turn failed trades or logs into concrete remediation tasks'
                '- Add environment drift checks for secrets, paper versus live settings, and deployment readiness before release work'
            )
        }
        'blog-post' = @{
            Tier1 = @(
                '- Add post type modes for how to, project update, troubleshooting writeup, and opinion pieces so the structure matches the goal faster'
                '- Add a stronger technical proof checklist that forces commands, screenshots, repo links, and validation evidence into implementation posts'
                '- Add title and intro variants that stay in Mick''s voice but offer a few tighter opening options'
            )
            Tier2 = @(
                '- Add SEO aware metadata output with slug, meta description, tags, and a suggested feature image concept'
                '- Add a cross link pass that suggests related blog posts, repo links, and follow on reading from the same topic area'
                '- Add beginner versus practitioner tone modes so the same topic can be written for different audiences'
            )
            Tier3 = @(
                '- Add a multi part series planner that can split a large topic into sequenced posts with consistent scope boundaries'
                '- Add source extraction from notes, transcripts, or repo files to build draft outlines automatically'
                '- Add content refresh mode for revisiting older posts and rewriting them when tools, platforms, or commands change'
            )
        }
        'blog-to-social' = @{
            Tier1 = @(
                '- Add per platform output controls for short, medium, and thread style variants so one post can be adapted cleanly'
                '- Add CTA selection rules that choose between discussion, click through, or save for later based on the blog topic'
                '- Add a hook quality pass that generates stronger first line options before the rest of the social copy'
            )
            Tier2 = @(
                '- Add image and carousel caption suggestions that pair the social copy with matching media ideas'
                '- Add excerpt selection logic that picks the best proof point or surprising detail from the source post'
                '- Add a scheduling note block with suggested publish order across Facebook, LinkedIn, and X'
            )
            Tier3 = @(
                '- Add campaign mode for turning one long post into a week of follow on social content'
                '- Add analytics feedback prompts so high performing posts can be reverse engineered into better future variants'
                '- Add support for newsletter and forum friendly versions beyond the current social targets'
            )
        }
        'container-home' = @{
            Tier1 = @(
                '- Add project phase modes for site prep, welding, framing, solar, plumbing, and interior planning so guidance is easier to target'
                '- Add a risk and dependency checklist for sequencing work items that can block later phases'
                '- Add materials and equipment planning output that separates must buy now from can wait items'
            )
            Tier2 = @(
                '- Add budget tracking prompts by build phase with rough order of magnitude cost buckets'
                '- Add code and permitting research checklists tailored to rural Tennessee build questions'
                '- Add off grid systems comparison output for batteries, inverter sizing, generator backup, and water handling'
            )
            Tier3 = @(
                '- Add a master build timeline mode that converts the project into staged milestones with dependencies'
                '- Add maintenance planning for long term ownership of the structure, solar system, and utilities'
                '- Add scenario planning for retirement occupancy, guest use, and future expansion options'
            )
        }
        'crypto-listings' = @{
            Tier1 = @(
                '- Add exchange priority tiers so listings from the most relevant venues are weighted higher in the output'
                '- Add catalyst quality scoring that separates confirmed listing announcements from rumor driven signals'
                '- Add a duplicate and stale event filter so repeated signals do not clutter the report'
            )
            Tier2 = @(
                '- Add watchlist mode for tracking specific coins across multiple exchanges and dates'
                '- Add expected impact notes that consider liquidity, exchange size, and prior listing patterns'
                '- Add structured output for importing listing events into a tracker or automation workflow'
            )
            Tier3 = @(
                '- Add historical listing outcome review to compare pre listing expectations with post listing performance'
                '- Add alert packaging for daily or weekly digests across multiple monitoring channels'
                '- Add exchange trust weighting so low credibility or thin volume sources are deprioritized automatically'
            )
        }
        'crypto-research' = @{
            Tier1 = @(
                '- Add a standardized token due diligence scorecard that forces fundamentals, tokenomics, team, and risk review every time'
                '- Add scam and red flag detection prompts for unlock risk, centralization, suspicious emissions, and governance theater'
                '- Add a compare mode for evaluating two projects side by side on the same rubric'
            )
            Tier2 = @(
                '- Add sector specific lenses for DeFi, infrastructure, gaming, AI, and meme coin research'
                '- Add portfolio fit guidance that frames a project as core, speculative, event driven, or avoid'
                '- Add reference tracking so thesis claims can be tied back to whitepapers, docs, and official announcements'
            )
            Tier3 = @(
                '- Add periodic thesis refresh prompts that re score a coin after major protocol, governance, or market changes'
                '- Add onchain metrics integration points for supply, holders, activity, and treasury analysis'
                '- Add a full research archive template so multiple coin reviews stay comparable over time'
            )
        }
        'facebook-post' = @{
            Tier1 = @(
                '- Add post modes for personal update, technical lesson, project progress, and opinion so the opening and structure match the goal'
                '- Add stronger hook generation for the first sentence with options that sound natural instead of promotional'
                '- Add length presets for short update, standard post, and longer story driven variants'
            )
            Tier2 = @(
                '- Add comment bait avoidance rules so engagement prompts stay natural and not forced'
                '- Add photo caption pairing guidance so the text matches build photos, screenshots, or workout images'
                '- Add audience mode switches for friends and family, technical peers, or mixed audiences'
            )
            Tier3 = @(
                '- Add series mode for recurring project updates with consistent structure across multiple posts'
                '- Add repurpose mode to turn a Facebook post into a matching blog or LinkedIn draft'
                '- Add feedback learning prompts based on which prior post types drew the best interaction'
            )
        }
        'facebook-reply' = @{
            Tier1 = @(
                '- Add reply tone modes for appreciative, clarifying, humorous, and boundary setting responses'
                '- Add context memory prompts so replies can account for the original post topic and who is being answered'
                '- Add concise versus fuller reply options to better match the comment depth'
            )
            Tier2 = @(
                '- Add difficult comment handling for skepticism, criticism, and off topic responses without escalating'
                '- Add CTA aware reply patterns for when Mick wants to move someone to DM, a blog link, or a follow up post'
                '- Add batch reply mode for multiple comments on the same post while keeping responses distinct'
            )
            Tier3 = @(
                '- Add thread summarization to detect repeated questions and draft one pinned clarification response'
                '- Add sentiment tagging so hostile, neutral, and supportive comments get different treatment'
                '- Add cross platform adaptation so strong replies can be reused in LinkedIn or X discussions'
            )
        }
        'fitness-log' = @{
            Tier1 = @(
                '- Add trend summaries for strength, endurance, consistency, and recovery across logged workouts'
                '- Add program check prompts that compare recent training against stated goals such as pull ups, cycling, or triathlon'
                '- Add fatigue and overload flags so the skill can call out when recent sessions suggest under recovery'
            )
            Tier2 = @(
                '- Add weekly review output with wins, missed sessions, and the next block focus'
                '- Add nutrition and timing prompts tied to workout type, duration, and recovery needs'
                '- Add better exercise normalization so similar movements are grouped more cleanly in progress reviews'
            )
            Tier3 = @(
                '- Add long horizon progression plans for race prep, strength cycles, and hybrid training seasons'
                '- Add export friendly structured data for dashboards or Obsidian tracking'
                '- Add injury and mobility tracking so training adjustments can account for recurring limitations'
            )
        }
        'food-analyzer' = @{
            Tier1 = @(
                '- Add confidence labels that separate obvious observations from low confidence guesses when the image or label is incomplete'
                '- Add goal aware output modes for fat loss, endurance fueling, muscle gain, and blood sugar control'
                '- Add a cleaner quick summary section before the deeper analysis so results are easier to scan'
            )
            Tier2 = @(
                '- Add comparison mode for two foods or meals with practical tradeoffs instead of only a single item analysis'
                '- Add meal timing guidance that changes based on pre workout, post workout, bedtime, or general daily use'
                '- Add better ingredient risk grouping for additives, sweeteners, seed oils, and ultra processed signals'
            )
            Tier3 = @(
                '- Add a meal history review mode that can look across repeated analyses and find patterns'
                '- Add export templates for logging summaries into notes or a nutrition tracker'
                '- Add user preference memory for favorite foods, sensitivities, and recurring supplement interactions'
            )
        }
        'github-readme' = @{
            Tier1 = @(
                '- Add repo archetype presets for PowerShell automation, Python app, hybrid repo, website, and template starter layouts'
                '- Add validation prompts that force the skill to check commands, paths, and file names against the live repo before writing'
                '- Add a README repair mode for stale docs that need targeted updates instead of a full rewrite'
            )
            Tier2 = @(
                '- Add beginner mode that explains setup steps more plainly when the repo targets less technical users'
                '- Add docs coverage checks for missing changelog, roadmap, project analysis, or spec references'
                '- Add output variants for concise project hubs versus detailed implementation guides'
            )
            Tier3 = @(
                '- Add repo wide README audit mode that walks subfolder docs, flags drift, and proposes a coordinated cleanup plan'
                '- Add installable template guidance for turning a live project into a reusable starter repo'
                '- Add link validation and cross file navigation checks as part of the writing workflow'
            )
        }
        'github-repo-architect' = @{
            Tier1 = @(
                '- Add stack specific scaffolding presets for PowerShell first automation repos, Python CLIs, hybrid repos, and static sites'
                '- Add stronger repo planning output for tracked versus local only docs such as changelogs, assessments, and future backlog files'
                '- Add test and CI recommendations that are opinionated enough to be directly implemented'
            )
            Tier2 = @(
                '- Add spec first project modes that emit numbered requirement, plan, task, and audit file structures by default'
                '- Add modernization mode for existing repos where the skill improves structure without pretending it is a greenfield project'
                '- Add repo risk review that highlights naming drift, folder sprawl, and missing validation paths before scaffolding'
            )
            Tier3 = @(
                '- Add architecture comparison mode that proposes two viable repo structures with tradeoffs'
                '- Add automation aware templates for n8n, homelab, AI skills, and endpoint management projects'
                '- Add migration playbooks for repos moving from ad hoc layouts into a more standardized structure'
            )
        }
        'github-social-preview' = @{
            Tier1 = @(
                '- Add theme presets beyond the current GitHub dark look so previews can better match the repo brand or project style'
                '- Add smarter text fitting and truncation for longer repo names, descriptions, and topic sets'
                '- Add a local preview checklist that verifies contrast, crop safety, and file size before final export'
            )
            Tier2 = @(
                '- Add support for optional accent color overrides based on the repo language or custom branding'
                '- Add batch mode for generating previews for multiple repositories in one run'
                '- Add alternate layouts optimized for docs repos, apps, and libraries with different emphasis'
            )
            Tier3 = @(
                '- Add dynamic asset support such as logos, screenshots, or custom background art when available'
                '- Add social preview variants for blog cards, release announcements, and project milestone posts'
                '- Add automated regression samples so design changes can be checked against known example repos'
            )
        }
        'idea-forge' = @{
            Tier1 = @(
                '- Add the next high value upgrade here'
            )
            Tier2 = @(
                '- Add the next medium effort upgrade here'
            )
            Tier3 = @(
                '- Add the next long term upgrade here'
            )
        }
        'linkedin-post' = @{
            Tier1 = @(
                '- Add post modes for career update, technical lesson, project breakdown, and opinion pieces'
                '- Add hook styles tuned for LinkedIn so the first two lines create interest without sounding inflated'
                '- Add credibility checks that push for proof, outcome, and context instead of vague claims'
            )
            Tier2 = @(
                '- Add CTA styles for hiring, networking, traffic to a repo, or simple discussion prompts'
                '- Add carousel and image companion copy suggestions for posts that need supporting media'
                '- Add tone controls for practitioner, leadership, and builder focused audiences'
            )
            Tier3 = @(
                '- Add content series planning for multi post project writeups or learning logs'
                '- Add audience testing variants to compare a more technical draft with a broader professional one'
                '- Add post to article expansion mode for turning strong short posts into longer form LinkedIn articles'
            )
        }
        'n8n-workflow' = @{
            Tier1 = @(
                '- Add workflow review mode that checks trigger choice, idempotency, retries, and failure handling before implementation'
                '- Add self hosted deployment guidance for secrets, backups, versioning, and environment promotion'
                '- Add a cleaner node by node build template for users who want exact wiring steps'
            )
            Tier2 = @(
                '- Add integration playbooks for common stacks such as webhooks, email, Slack, databases, and AI APIs'
                '- Add troubleshooting output that maps common n8n runtime failures to likely root causes'
                '- Add reusable subworkflow guidance so larger automations stay maintainable'
            )
            Tier3 = @(
                '- Add architecture mode for multi workflow systems with queueing, persistence, and monitoring'
                '- Add migration guidance for moving manual processes or scripts into n8n step by step'
                '- Add test strategy suggestions for validating workflows safely before production use'
            )
        }
        'obsidian-workout-export' = @{
            Tier1 = @(
                '- Add template variants for strength sessions, rides, runs, and combined training days'
                '- Add better metadata fields for tags, effort, duration, and progression notes'
                '- Add duplicate protection rules so repeated exports do not create messy note histories'
            )
            Tier2 = @(
                '- Add vault structure presets so exports can target daily notes, workout folders, or program folders'
                '- Add summary block generation for PRs, weekly trends, and recovery notes'
                '- Add import cleanup for inconsistent exercise names and unit formatting'
            )
            Tier3 = @(
                '- Add bidirectional sync ideas between Obsidian notes and a structured workout log source'
                '- Add chart ready table output for tracking performance over time'
                '- Add companion export paths for race planning and training block reviews'
            )
        }
        'photo-rename' = @{
            Tier1 = @(
                '- Add stronger filename rules for date, location, event, and subject ordering so results stay consistent'
                '- Add confidence handling for unclear images where the subject or place is only partially identifiable'
                '- Add collision safe rename behavior that handles duplicate names without manual cleanup'
            )
            Tier2 = @(
                '- Add batch review mode that groups similar images and applies more consistent naming across a set'
                '- Add optional keyword extraction for later search and archive filtering'
                '- Add better fallback behavior when GPS metadata is missing or obviously wrong'
            )
            Tier3 = @(
                '- Add event level renaming that can infer a shared trip or build session across many photos'
                '- Add export reports showing old names, new names, and confidence reasons'
                '- Add sidecar metadata writing for tools that use keywords or captions beyond filenames'
            )
        }
        'pihole-blocklist' = @{
            Tier1 = @(
                '- Add a source scoring rubric that weights trust, overlap, maintenance, and false positive risk more explicitly'
                '- Add category recommendation output that proposes the exact repo placement for a new source'
                '- Add a quick reject checklist for abandoned, duplicate, or low quality lists'
            )
            Tier2 = @(
                '- Add change review mode for existing sources that have grown or shifted scope over time'
                '- Add allowlist impact guidance when a strong source might still break common services'
                '- Add maintainer health checks that look at update frequency and project transparency'
            )
            Tier3 = @(
                '- Add automation friendly output for turning evaluations into tracked repo tasks'
                '- Add historical source comparison to spot which providers age well versus create cleanup churn'
                '- Add policy presets for strict privacy, balanced default, and aggressive blocking stacks'
            )
        }
        'pihole-csv-analyzer' = @{
            Tier1 = @(
                '- Add clearer prioritization of noisy domains, likely false positives, and high leverage cleanup targets'
                '- Add device or client level grouping so problem traffic can be traced to the right source faster'
                '- Add recommended action output that separates block, allow, investigate, and ignore paths'
            )
            Tier2 = @(
                '- Add recurring pattern detection for domains that appear during updates, streaming, or app startup'
                '- Add summary exports suitable for repo notes or maintenance logs'
                '- Add comparison mode between two CSV exports to show what changed after list updates'
            )
            Tier3 = @(
                '- Add long term trend analysis across multiple export files'
                '- Add source attribution hints to map blocked domains back to likely blocklists when possible'
                '- Add workflow handoff to pihole-blocklist for deciding whether cleanup should change the curated sources'
            )
        }
        'proxmox-lxc' = @{
            Tier1 = @(
                '- Add container recipe modes for common services with storage, networking, and update guidance'
                '- Add pre deployment checks for CPU, RAM, disk, VLAN, and privilege choices before recommending a build'
                '- Add backup and rollback guidance so changes are easier to test safely'
            )
            Tier2 = @(
                '- Add security hardening suggestions for unprivileged containers, mounts, and exposed services'
                '- Add troubleshooting output for DNS, storage permission, startup, and package install failures'
                '- Add migration guidance for moving a service from VM to LXC or between hosts'
            )
            Tier3 = @(
                '- Add homelab architecture mode for multiple LXCs with shared reverse proxy, monitoring, and backup patterns'
                '- Add lifecycle planning for patching, snapshots, and template maintenance'
                '- Add service catalog templates tailored to Mick''s current self hosted stack'
            )
        }
        'resume-writer' = @{
            Tier1 = @(
                '- Add a job fit scoring summary that shows how well the resume matches the target role before and after the rewrite'
                '- Add stronger bullet rewrite guidance for quantifying impact when the original resume is too vague'
                '- Add a recruiter skim view that summarizes the top proof points in the first 30 seconds'
            )
            Tier2 = @(
                '- Add role family presets for infrastructure, endpoint engineering, cloud, support escalation, and leadership tracks'
                '- Add LinkedIn profile alignment guidance so the resume and profile do not drift apart'
                '- Add ATS keyword balance checks that improve match quality without turning the resume into keyword spam'
            )
            Tier3 = @(
                '- Add interview prep handoff so the resume rewrite can feed likely question prompts and talking points'
                '- Add career timeline consistency checks across resume, LinkedIn, and cover letter artifacts'
                '- Add longitudinal improvement tracking for repeated resume revisions over time'
            )
        }
        'travel-itinerary' = @{
            Tier1 = @(
                '- Add itinerary templates for city trip, road trip, active travel, and mixed work plus leisure trips'
                '- Add daily structure checks so transit time, meals, and activity pacing are more realistic'
                '- Add packing and reservation summaries that roll up the critical trip details cleanly'
            )
            Tier2 = @(
                '- Add map and route note blocks that make moving between stops easier to follow'
                '- Add budget visibility per day and per category'
                '- Add contingency notes for weather, delays, and backup activities'
            )
            Tier3 = @(
                '- Add multi traveler coordination output for shared plans and responsibility splits'
                '- Add handoff formats for Obsidian, printable trip sheets, and mobile friendly summaries'
                '- Add post trip review prompts to improve future itineraries from what actually happened'
            )
        }
        'travel-planning' = @{
            Tier1 = @(
                '- Add destination comparison mode that scores options against budget, training goals, climate, and interests'
                '- Add trip style presets for endurance travel, sightseeing, remote work, and minimalist carry only travel'
                '- Add planning output that clearly separates must book now from research later'
            )
            Tier2 = @(
                '- Add seasonal guidance for when a destination is great, crowded, expensive, or poor value'
                '- Add risk notes for transit complexity, safety, visa friction, and overpacked itineraries'
                '- Add companion packing and gear suggestions tied to the trip type'
            )
            Tier3 = @(
                '- Add long horizon country goal planning for the 50 country target'
                '- Add repeatable budget benchmarking across multiple destination candidates'
                '- Add integration with itinerary output so planning can flow directly into a day by day trip plan'
            )
        }
        'website-content' = @{
            Tier1 = @(
                '- Add page type modes for home page, about page, service page, project page, and contact copy'
                '- Add stronger proof and specificity checks so claims are backed by examples, repos, or outcomes'
                '- Add concise versus detailed copy variants for the same section depending on layout constraints'
            )
            Tier2 = @(
                '- Add brand voice controls for technical, personal, builder focused, and professional audience mixes'
                '- Add CTA suggestions that match whether the page is meant for contact, trust building, or portfolio browsing'
                '- Add SEO aware title and meta description output for each page draft'
            )
            Tier3 = @(
                '- Add full site consistency review across multiple pages and reused copy blocks'
                '- Add project library extraction so portfolio entries can be drafted from repo notes or changelogs'
                '- Add refresh mode for revisiting outdated pages after new projects or career changes'
            )
        }
        'x-post' = @{
            Tier1 = @(
                '- Add length presets for single post, short thread opener, and punchier one line variants'
                '- Add hook generation tuned for X so the first clause lands quickly without sounding forced'
                '- Add topic modes for PowerShell, endpoint management, fitness, and build project updates'
            )
            Tier2 = @(
                '- Add reply bait awareness so the post invites discussion without sounding engagement hungry'
                '- Add thread follow up suggestions when the topic needs more space than one post'
                '- Add companion media notes for screenshots, code clips, charts, or project photos'
            )
            Tier3 = @(
                '- Add adaptation mode to turn a strong X post into matching LinkedIn or Facebook copy'
                '- Add performance review prompts based on prior post styles that worked well'
                '- Add event driven posting templates for launches, race results, and build milestones'
            )
        }
        'x-reply' = @{
            Tier1 = @(
                '- Add reply modes for agreement, clarification, respectful disagreement, and quick thank you responses'
                '- Add quote tweet versus direct reply guidance so the best response format is chosen intentionally'
                '- Add brevity controls so replies stay sharp when the conversation moves fast'
            )
            Tier2 = @(
                '- Add context carryover from the original post and thread tone before drafting the reply'
                '- Add escalation handling for hostile or baiting replies where the best move may be not to engage'
                '- Add batch reply drafting for several mentions on the same topic'
            )
            Tier3 = @(
                '- Add thread summarization so repeated questions can be handled with one stronger response'
                '- Add persona tuning for technical, casual, and builder focused interactions'
                '- Add reuse prompts for turning good replies into future standalone post ideas'
            )
        }
    }

    if ($map.ContainsKey($SkillName)) {
        return $map[$SkillName]
    }

    return @{
        Tier1 = @('- Add the next high value upgrade here')
        Tier2 = @('- Add the next medium effort upgrade here')
        Tier3 = @('- Add the next long term upgrade here')
    }
}

function New-FutureUpgradesContent {
    param(
        [string]$SkillName,
        [hashtable]$PreservedContent
    )

    $today = Get-Date -Format 'yyyy-MM-dd'
    $defaultSuggestions = Get-DefaultTierSuggestions -SkillName $SkillName
    $tier1 = Get-TierBody -Lines $PreservedContent['## Tier 1: High Value'] -Placeholder ($defaultSuggestions.Tier1 -join [Environment]::NewLine)
    $tier2 = Get-TierBody -Lines $PreservedContent['## Tier 2: Medium Value'] -Placeholder ($defaultSuggestions.Tier2 -join [Environment]::NewLine)
    $tier3 = Get-TierBody -Lines $PreservedContent['## Tier 3: Long Term'] -Placeholder ($defaultSuggestions.Tier3 -join [Environment]::NewLine)

    @"
# Future Upgrades: $SkillName

This file is local planning for future work.

Last auto update: $today

## Recent Completed Work

- See [completedchanges.md](completedchanges.md) for tracked completed history.

## Tier 1: High Value

$tier1

## Tier 2: Medium Value

$tier2

## Tier 3: Long Term

$tier3
"@.Trim() + [Environment]::NewLine
}

$resolvedSkillsRoot = (Resolve-Path -LiteralPath $SkillsRoot).Path
$skillDirectories = @(Get-SkillDirectories -Path $resolvedSkillsRoot)
$updatedCount = 0

foreach ($directory in $skillDirectories) {
    $futurePath = Join-Path $directory.FullName 'future-upgrades.md'
    $preservedContent = Get-PreservedTierContent -FuturePath $futurePath
    $newContent = New-FutureUpgradesContent -SkillName $directory.Name -PreservedContent $preservedContent
    $currentContent = if (Test-Path -LiteralPath $futurePath) { Get-Content -LiteralPath $futurePath -Raw } else { '' }

    if ($currentContent -ceq $newContent) {
        continue
    }

    if ($PSCmdlet.ShouldProcess($futurePath, 'Update future upgrades file')) {
        Set-Content -LiteralPath $futurePath -Value $newContent -Encoding utf8
        $updatedCount++
    }
}

Write-Host "Processed skill folders: $($skillDirectories.Count)"
Write-Host "Updated future-upgrades files: $updatedCount"
