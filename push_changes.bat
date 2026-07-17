@echo off
:: Enable UTF-8 encoding in command prompt
chcp 65001 > nul

echo =======================================================
echo   EDO LMS - Professional Git va GitHub-ga yuklash
echo =======================================================
echo.

:: 1. Git faolligini tekshirish
if not exist .git (
    echo [INFO] Git repozitoriyasi topilmadi. Yangi repozitoriya yaratilmoqda...
    git init
    if errorlevel 1 (
        echo [ERROR] Git-ni yaratishda xatolik yuz berdi.
        goto end
    )
) else (
    echo [OK] Git repozitoriyasi allaqachon mavjud.
)

:: 2. Masofaviy repozitoriya (remote origin) sozlash
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo [INFO] Masofaviy remote origin qo'shilmoqda...
    git remote add origin https://github.com/Valijon21/edo_lms_app.git
) else (
    echo [OK] Remote origin allaqachon sozlangan: https://github.com/Valijon21/edo_lms_app.git
)

:: 3. O'zgarishlarni kiritish (.gitignore asosida keraksiz fayllar tashlab ketiladi)
echo.
echo [INFO] Yangi va o'zgargan fayllar qo'shilmoqda (git add .)...
git add .

:: 4. Commit qilish
echo.
set /p commit_msg="Iltimos, commit xabarini kiriting (bo'sh qoldirilsa avtomatik xabar beriladi): "
if "%commit_msg%"=="" (
    set commit_msg="feat: initial project structure with professional gitignore and documentation"
)

echo [INFO] Commit qilinmoqda: %commit_msg%...
git commit -m "%commit_msg%"

:: 5. Main branch yaratish va tekshirish
git branch -M main

:: 6. GitHub-ga push qilish
echo.
echo =======================================================
echo   GitHub-ga yuklash (git push origin main)...
echo   (Agar kerak bo'lsa, sizdan GitHub paroli yoki Token so'ralishi mumkin)
echo =======================================================
git push -u origin main

if errorlevel 1 (
    echo.
    echo [ERROR] Kodni GitHub-ga yuklashda xatolik yuz berdi!
    echo Iltimos, quyidagilarni tekshiring:
    echo  1. Internet aloqasi va GitHub-da repozitoriya yaratilganligi.
    echo  2. SSH yoki HTTPS orqali GitHub-ga kirish ruxsati borligi.
    goto end
)

echo.
echo =======================================================
echo   [SUCCESS] O'zgarishlar muvaffaqiyatli yuklandi!
echo =======================================================

:end
echo.
pause
