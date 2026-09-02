# T-AIR - everything that has to run on this machine, in one script.
#
#   .\publish.ps1
#
# Fetches the typefaces, rebuilds, runs the checks, commits, and pushes to
# GitHub. It does not create the repository or turn on Pages - both are two
# clicks in a browser.
#
# Messages are in English on purpose: the Windows console mangles Persian.
# Nothing here is destructive; if a step fails you can just run it again.

$ErrorActionPreference = "Stop"

function Say($m)  { Write-Host "`n$m" -ForegroundColor Cyan }
function Warn($m) { Write-Host "  $m" -ForegroundColor Yellow }
function Good($m) { Write-Host "  $m" -ForegroundColor Green }
function Bad($m)  { Write-Host "  $m" -ForegroundColor Red }

Say "1. Checking what is installed"

try { $null = git --version } catch {
  Bad "git is not installed: https://git-scm.com/download/win"; exit 1
}
Good "git found"

$py = $null
foreach ($c in @("python", "python3", "py")) {
  try { $null = & $c --version 2>$null; if ($LASTEXITCODE -eq 0) { $py = $c; break } } catch { }
}
if (-not $py) {
  Bad "python is not installed: https://www.python.org/downloads/"
  Bad "tick 'Add python.exe to PATH' during setup"
  exit 1
}
Good "python found ($py)"

if (-not (Test-Path "index.html")) {
  Bad "This is not the project folder - run it where index.html is."
  exit 1
}

$name = git config user.name
if (-not $name) {
  git config user.name "Taha"
  git config user.email "t7693903@gmail.com"
  $name = "Taha"
}
Good "commits will be authored by $name"

Say "2. Self-hosting the typefaces"
Write-Host "   Why: while the fonts come from Google's servers, a visitor who"
Write-Host "   cannot reach them sees the site in the browser's default font."

& $py -m pip install --quiet --disable-pip-version-check requests pillow
$fontsOk = $true
try { & $py scripts\fetch_fonts.py; if ($LASTEXITCODE -ne 0) { $fontsOk = $false } }
catch { $fontsOk = $false }
if ($fontsOk) {
  Good "fonts are in the repository"
} else {
  Warn "Could not reach Google Fonts. Carrying on without them."
  Warn "You can do it later on GitHub: Actions -> Fetch fonts and photographs."
}

Say "3. Rebuilding and running the checks"
& $py scripts\merge_parts.py
& $py scripts\build_data.py
& $py scripts\test_build.py
if ($LASTEXITCODE -ne 0) { Bad "A data check failed - stopping."; exit 1 }
& $py scripts\build_single.py
& $py scripts\build_pages.py
Good "all data checks passed"

Say "4. Committing"
if (git status --porcelain) {
  git add -A
  git commit -m "Self-host the typefaces and rebuild"
  Good "committed"
} else {
  Good "nothing to commit"
}

Say "5. Pushing to GitHub"
$remote = git remote get-url origin 2>$null
if (-not $remote) {
  $user = Read-Host "GitHub username"
  if (-not $user) { Bad "Cannot push without it."; exit 1 }
  git remote add origin "https://github.com/$user/t-air.git"
  $remote = git remote get-url origin
}
Good "remote: $remote"
git branch -M main
git push -u origin main
if ($LASTEXITCODE -ne 0) {
  Bad "The push failed. Copy the message above into the chat."
  exit 1
}

$user = ($remote -replace ".*github\.com[:/]", "") -replace "/.*", ""
Say "Done."
Write-Host @"
  One thing left, in the browser:

     repository -> Settings -> Pages
     Source: Deploy from a branch
     Branch: main    Folder: / (root)    -> Save

  A minute or two later the site is at:

     https://$user.github.io/t-air/

  Fonts and photographs can then be fetched on GitHub itself:
     Actions -> Fetch fonts and photographs -> Run workflow
"@ -ForegroundColor Green
