# T-AIR — یک اسکریپت برای همه‌ی کارهایی که روی این کامپیوتر انجام می‌شود.
#
#   در PowerShell، داخل همین پوشه:
#       .\publish.ps1
#
# چه می‌کند: فونت‌ها را محلی می‌کند، سایت را دوباره می‌سازد، بررسی‌ها را اجرا
# می‌کند، کامیت می‌زند، مخزن را به GitHub وصل می‌کند و پوش می‌کند.
#
# چه نمی‌کند: مخزن را روی GitHub نمی‌سازد و Pages را روشن نمی‌کند — هر دو کار
# دو کلیک در مرورگرند و اسکریپت سر جایش می‌ایستد تا انجامشان بدهید.
#
# اگر وسط کار خطا خورد، هیچ چیزی خراب نمی‌شود: هر مرحله جداست و می‌توانید
# دوباره اجرایش کنید.

$ErrorActionPreference = "Stop"

function Say($msg)  { Write-Host "`n$msg" -ForegroundColor Cyan }
function Warn($msg) { Write-Host "  $msg" -ForegroundColor Yellow }
function Good($msg) { Write-Host "  $msg" -ForegroundColor Green }

# --------------------------------------------------------------- پیش‌نیازها
Say "بررسی پیش‌نیازها"

try { $null = git --version } catch {
  Write-Host "git نصب نیست: https://git-scm.com/download/win" -ForegroundColor Red; exit 1
}
Good "git هست"

$py = $null
foreach ($c in @("python", "python3", "py")) {
  try { $null = & $c --version 2>$null; $py = $c; break } catch { }
}
if (-not $py) {
  Write-Host "python نصب نیست: https://www.python.org/downloads/" -ForegroundColor Red
  Write-Host "موقع نصب تیک 'Add python.exe to PATH' را بزنید." -ForegroundColor Red
  exit 1
}
Good "python هست ($py)"

if (-not (Test-Path "index.html")) {
  Write-Host "این پوشه پروژه نیست. داخل پوشه‌ای اجرا کنید که index.html دارد." -ForegroundColor Red
  exit 1
}

# ------------------------------------------------------------------ هویت git
$name = git config user.name
if (-not $name) {
  $name = Read-Host "نام شما برای کامیت‌ها"
  git config user.name $name
  $mail = Read-Host "ایمیل شما"
  git config user.email $mail
}
Good "کامیت‌ها به نام $name ثبت می‌شوند"

# -------------------------------------------------------------------- فونت‌ها
Say "محلی کردن فونت‌ها"
Write-Host "  چرا: تا وقتی فونت از سرور گوگل می‌آید، بازدیدکننده‌ای که به آن"
Write-Host "  دسترسی ندارد سایت را با فونت پیش‌فرض مرورگر می‌بیند."

& $py -m pip install --quiet requests pillow
$fontsOk = $true
try { & $py scripts\fetch_fonts.py } catch { $fontsOk = $false }
if (-not $fontsOk) {
  Warn "به Google Fonts نرسیدیم. اگر VPN دارید، روشنش کنید و بعداً"
  Warn "فقط این را بزنید:  $py scripts\fetch_fonts.py"
  Warn "فعلاً بدون آن ادامه می‌دهیم — سایت کار می‌کند، فقط فونتش از گوگل می‌آید."
} else {
  Good "فونت‌ها داخل مخزن آمدند"
}

# --------------------------------------------------------------- ساخت و تست
Say "ساخت دوباره و اجرای بررسی‌ها"
& $py scripts\merge_parts.py
& $py scripts\build_data.py
& $py scripts\test_build.py
& $py scripts\build_single.py
& $py scripts\build_pages.py
Good "همه‌ی بررسی‌های داده پاس شد"

# -------------------------------------------------------------------- کامیت
$dirty = git status --porcelain
if ($dirty) {
  git add -A
  git commit -m "Self-host the typefaces and rebuild"
  Good "کامیت ثبت شد"
} else {
  Good "چیزی برای کامیت نبود"
}

# ------------------------------------------------------------------ اتصال
Say "اتصال به GitHub"
$remote = git remote get-url origin 2>$null
if (-not $remote) {
  Write-Host "  مخزن باید از قبل روی GitHub ساخته شده باشد: https://github.com/new"
  Write-Host "  نام t-air ، حالت Public ، و هیچ‌کدام از تیک‌های README/gitignore/license را نزنید."
  $user = Read-Host "`nنام کاربری GitHub شما"
  if (-not $user) { Write-Host "بدون نام کاربری نمی‌شود ادامه داد." -ForegroundColor Red; exit 1 }
  git remote add origin "https://github.com/$user/t-air.git"
  $remote = "https://github.com/$user/t-air.git"
}
Good "مقصد: $remote"

Say "پوش"
git branch -M main
git push -u origin main

# ------------------------------------------------------------------ پایان
$user = ($remote -replace ".*github\.com[:/]", "") -replace "/.*", ""
Say "تمام شد"
Write-Host @"
  یک کار در مرورگر مانده:

    مخزن → Settings → Pages
    Source: Deploy from a branch
    Branch: main   Folder: / (root)   →  Save

  یکی دو دقیقه بعد سایت اینجاست:

    https://$user.github.io/t-air/

  بعد از اینکه بالا آمد، برای عکس‌ها:

    $py scripts\fetch_photos.py
    $py scripts\build_single.py
    git add -A ; git commit -m "Add photograph library" ; git push
"@ -ForegroundColor Green
