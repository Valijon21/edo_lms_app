@echo off
echo =======================================================
echo  Django Migrations va Seed Ma'lumotlarini Ishga Tushirish
echo =======================================================
echo.

echo 1. Yangi migration fayllarini yaratish (makemigrations)...
.venv\Scripts\python.exe manage.py makemigrations
if %errorlevel% neq 0 (
    echo.
    echo [XATO] Migration yaratishda xatolik yuz berdi!
    goto error
)
echo.

echo 2. Migrationlarni bazaga qo'llash (migrate)...
.venv\Scripts\python.exe manage.py migrate
if %errorlevel% neq 0 (
    echo.
    echo [XATO] Migrationlarni qo'llashda xatolik yuz berdi!
    goto error
)
echo.

echo 3. Seed ma'lumotlarini bazaga yuklash (seed_lessons.py)...
.venv\Scripts\python.exe seed_lessons.py
if %errorlevel% neq 0 (
    echo.
    echo [XATO] Seed ma'lumotlarini yuklashda xatolik yuz berdi!
    goto error
)
echo.

echo =======================================================
echo  MUVAFFAQIYATLI YAKUNLANDI!
echo =======================================================
echo Barcha topshiriqlar bajarildi, bazaga seed savollar yuklandi.
goto end

:error
echo.
echo [XATO] Jarayon muvaffaqiyatsiz yakunlandi. Iltimos, xatoliklarni tekshiring.
echo.

:end
pause
