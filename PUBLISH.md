# انتشار روی GitHub — گام به گام

مخزن اینجا از قبل ساخته شده و کامیت خورده است. فقط باید به GitHub وصلش کنی.

## ۱. مخزن را روی GitHub بساز

در <https://github.com/new> یک مخزن **خالی** بساز — بدون README، بدون
`.gitignore`، بدون LICENSE، چون همه‌شان اینجا هستند. اسم پیشنهادی: `t-air`.

## ۲. وصل کن و پوش کن

در پوشه‌ی پروژه:

```bash
git remote add origin https://github.com/<USERNAME>/t-air.git
git branch -M main
git push -u origin main
```

اگر GitHub رمز خواست، رمز حساب کار نمی‌کند؛ باید یک
[personal access token](https://github.com/settings/tokens) با دسترسی `repo`
بسازی و به‌جای رمز بزنی.

## ۳. GitHub Pages را روشن کن

در مخزن: **Settings → Pages**

- **Source**: `Deploy from a branch`
- **Branch**: `main` و پوشه‌ی `/ (root)`
- **Save**

یکی دو دقیقه بعد سایت اینجا بالا می‌آید:

```
https://<USERNAME>.github.io/t-air/
```

## ۴. عکس‌ها را اضافه کن

سایت بدون عکس محلی هم کار می‌کند، ولی با عکس خیلی بهتر است. یک بار:

```bash
pip install pillow requests
python3 scripts/fetch_photos.py      # حدود ۴۰ تا ۵۰ مگابایت، قابل ازسرگیری
python3 scripts/build_single.py
git add assets/photos data/photos.json dist
git commit -m "Add photograph library"
git push
```

به‌محض اینکه عکس‌ها بیایند، کارت‌های نتایج هم نوار عکس می‌گیرند.

## ۵. فونت‌ها را محلی کن (توصیه‌ی جدی)

تا وقتی صفحه فونت را از Google Fonts می‌گیرد، بازدیدکننده‌ای که به سرورهای گوگل
دسترسی ندارد — یعنی بخش بزرگی از مخاطب ایرانی این سایت — صفحه را با فونت پیش‌فرض
مرورگر می‌بیند. یک بار:

```bash
pip install requests
python3 scripts/fetch_fonts.py
python3 scripts/build_single.py
git add assets/fonts assets/fonts.css index.html dist
git commit -m "Self-host the typefaces"
git push
```

حدود ۴۰۰ کیلوبایت به مخزن اضافه می‌شود، `index.html` خودش به `assets/fonts.css`
وصل می‌شود و CSP هم دیگر به دامنه‌های گوگل اجازه نمی‌دهد. هر چهار فونت با مجوز
SIL OFL هستند و متن مجوز کنارشان نوشته می‌شود.

اگر خودِ Google Fonts هم برایتان باز نمی‌شود، این یک مرحله را با VPN اجرا کنید؛
بعدش دیگر هیچ‌وقت لازم نیست.

## ۶. آدرس‌های مطلق را درست کن (اختیاری)

بعد از اینکه آدرس نهایی را داشتی، در `index.html` این خط را کامل کن تا
پیش‌نمایش لینک در تلگرام و توییتر درست بیفتد:

```html
<meta property="og:image" content="assets/social-card.png">
```

به:

```html
<meta property="og:image" content="https://<USERNAME>.github.io/t-air/assets/social-card.png">
```

## پیش از هر کامیت

```bash
bash scripts/check.sh
```

این دستور داده را دوباره می‌سازد، ۳۵ بررسی دیتابیس و — در صورت نصب‌بودن
Playwright — ۲۴ بررسی رابط را اجرا می‌کند، و نسخه‌ی تک‌فایلی را به‌روز می‌کند. همین بررسی‌ها روی GitHub هم با
هر پوش اجرا می‌شوند (`.github/workflows/checks.yml`).

## دامنه‌ی اختصاصی (اختیاری)

اگر دامنه داری: در **Settings → Pages → Custom domain** آدرس را بزن، و یک
رکورد `CNAME` در DNS به `<USERNAME>.github.io` بساز. GitHub خودش فایل `CNAME`
را در مخزن می‌سازد.
