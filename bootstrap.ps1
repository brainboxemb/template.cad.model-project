<#
.SYNOPSIS
    Install the Forge release pinned by this CAD repository.
.DESCRIPTION
    Reads dependencies.forge and dependencies.solidcraft from ci.yml.
    The readable Forge release tag is used for local installation, but is
    accepted only when it resolves to the exact immutable commit pinned for CI.
#>
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$configPath = Join-Path $root 'ci.yml'

if (-not (Test-Path -LiteralPath $configPath -PathType Leaf)) {
    throw "Missing $configPath"
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw 'Git is required.'
}
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw 'Python must be available in the active environment.'
}

$source = Get-Content -LiteralPath $configPath -Raw
$forgeMatch = [regex]::Match(
    $source,
    '(?ms)^  forge:\s*\r?\n(?<body>.*?)(?=^  solidcraft:)'
)
if (-not $forgeMatch.Success) {
    throw 'Missing dependencies.forge in ci.yml'
}
$forge = $forgeMatch.Groups['body'].Value

function Read-ForgeValue([string]$Name) {
    $match = [regex]::Match(
        $forge,
        "(?m)^    $([regex]::Escape($Name)):\s*(\S+)\s*$"
    )
    if (-not $match.Success) {
        throw "Missing dependencies.forge.$Name in ci.yml"
    }
    return $match.Groups[1].Value.Trim()
}

$repository = Read-ForgeValue 'repository'
$release = Read-ForgeValue 'release'
$version = Read-ForgeValue 'version'
$commit = (Read-ForgeValue 'commit').ToLowerInvariant()

if ($release -notmatch '^v\d+\.\d+\.\d+$') {
    throw "Forge release must be a v-prefixed semver tag; found $release"
}
if ($commit -notmatch '^[0-9a-f]{40}$') {
    throw "Forge commit must be an exact 40-character SHA; found $commit"
}

$remote = "https://github.com/$repository.git"
$tagRef = "refs/tags/$release"
$derefRef = "$tagRef^{}"

$lines = & git ls-remote --tags $remote $tagRef $derefRef
if ($LASTEXITCODE -ne 0) {
    throw "Cannot resolve Forge release $release from $remote"
}

$resolved = $null
foreach ($line in $lines) {
    $parts = $line -split '\s+'
    if ($parts.Count -lt 2) { continue }
    $sha = $parts[0].ToLowerInvariant()
    $ref = $parts[1]
    if ($ref -eq $derefRef) {
        $resolved = $sha
        break
    }
    if ($ref -eq $tagRef -and -not $resolved) {
        $resolved = $sha
    }
}

if (-not $resolved) {
    throw "Forge release tag $release was not found"
}
if ($resolved -ne $commit) {
    throw "Forge release $release resolves to $resolved, but ci.yml pins $commit"
}

$install = "git+$remote@$release#subdirectory=scpf"
& python -m pip install --disable-pip-version-check --no-deps --upgrade --force-reinstall $install
if ($LASTEXITCODE -ne 0) {
    throw "Failed to install Forge $release"
}

$actualVersion = (& python -c "from importlib.metadata import version; print(version('scpf'))").Trim()
if ($LASTEXITCODE -ne 0 -or $actualVersion -ne $version) {
    throw "SCPF version mismatch: expected $version, found $actualVersion"
}

$solidcraftMatch = [regex]::Match(
    $source,
    '(?ms)^  solidcraft:\s*\r?\n(?<body>.*?)(?=^\S|\z)'
)
if (-not $solidcraftMatch.Success) {
    throw 'Missing dependencies.solidcraft in ci.yml'
}
$scVersionMatch = [regex]::Match(
    $solidcraftMatch.Groups['body'].Value,
    '(?m)^    version:\s*(\S+)\s*$'
)
if (-not $scVersionMatch.Success) {
    throw 'Missing dependencies.solidcraft.version in ci.yml'
}
$expectedSolidCraft = $scVersionMatch.Groups[1].Value.Trim()
$qualifiedSolidCraft = (& python -c "from scpf.version import TESTED_SOLIDCRAFT_VERSION; print(TESTED_SOLIDCRAFT_VERSION)").Trim()
if ($LASTEXITCODE -ne 0 -or $qualifiedSolidCraft -ne $expectedSolidCraft) {
    throw "Forge $release qualifies SolidCraft $qualifiedSolidCraft, but ci.yml pins $expectedSolidCraft"
}

Write-Host "Ready: Forge $release (SCPF $actualVersion) at $commit"
Write-Host "Qualified SolidCraft: $qualifiedSolidCraft"
