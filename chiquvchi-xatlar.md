# Plan: Chiquvchi xatlar darsini tizimga qo'shish

## Overview
Ushbu reja Ijro.uz o'quv platformasida chiquvchi hujjatlar (xatlar) bilan ishlash bo'yicha 3-darsni va unga doir test savollarini qo'shish jarayonini qamrab oladi. Loyihada tayyor video fayl (`EDO IJRO UZ chiquvchi xatlar - Ibrohim Karimov (720p, h264) (1).mp4`) mavjud bo'lib, uning kadrlari allaqachon `media/courses/chiquvchi_xatlar/` papkasiga yuklangan. Reja doirasida ushbu darsning transkripsiyasi amalga oshiriladi, dars mazmuni yoziladi, ma'lumotlar ombori uchun test savollari shakllantiriladi va barchasi `seed_lessons.py` orqali tizimga seed qilinadi.

## Project Type
- **WEB** (Django 5.x)

## Success Criteria
- [ ] Chiquvchi xatlar bo'yicha transkript to'liq shakllantiriladi va `media/transcripts/chiquvchi_xatlar_transcript.txt` faylida saqlanadi.
- [ ] Tizimda yangi modul (`2-Modul: Chiquvchi hujjatlar bilan ishlash`) va uning 1-darsi (`Chiquvchi xatlarni yaratish va jo'natish`) yaratiladi.
- [ ] Dars tarkibida qadam-baqadam skrinshotlar (`media/courses/chiquvchi_xatlar/frame_*.jpg`) va tushuntirishlar html shaklida shakllantiriladi.
- [ ] Yangi modul uchun kamida 4 ta test savollari va javob variantlari yaratiladi.
- [ ] `seed_lessons.py` skripti yangilanib, ishga tushirilganda ma'lumotlar muvaffaqiyatli saqlanadi.
- [ ] Barcha pytest testlari muvaffaqiyatli o'tadi.

## Tech Stack
- Django 5.x, SQLite (Dev DB)
- Python 3.12 (faster-whisper, PyAV, opencv-python)

## File Structure
Yangi/o'zgaradigan fayllar joylashuvi:
```
c:\Users\nout.plus\Desktop\Proyekt\edo\
├── media/
│   ├── transcripts/
│   │   └── chiquvchi_xatlar_transcript.txt    # [MODIFY] yangi transkript yoziladi
├── seed_lessons.py                              # [MODIFY] yangi modul, dars va testlar qo'shiladi
```

## Task Breakdown

### Task 1: Transkripsiya yakunlanishi va matnni saqlash
- **Agent**: `backend-specialist`
- **Skills**: `clean-code`, `python-patterns`
- **Priority**: High
- **Dependencies**: None
- **INPUT**: `EDO IJRO UZ chiquvchi xatlar - Ibrohim Karimov (720p, h264) (1).mp4` videosi va `process_new_lesson.py` skripti.
- **OUTPUT**: `media/transcripts/chiquvchi_xatlar_transcript.txt` faylida transkripsiya matnining shakllanishi.
- **VERIFY**: Transkript fayli mavjudligi va 0 byte dan kattaligini tekshirish.

### Task 2: Seeding skriptini (`seed_lessons.py`) yangilash
- **Agent**: `database-architect`
- **Skills**: `database-design`, `clean-code`
- **Priority**: High
- **Dependencies**: Task 1
- **INPUT**: Transkript matni va extracted keyframes (`media/courses/chiquvchi_xatlar/` ichida).
- **OUTPUT**: Yangilangan `seed_lessons.py` fayli, unda:
  - `2-Modul: Chiquvchi hujjatlar bilan ishlash` yaratiladi.
  - `Chiquvchi xatlarni yaratish va jo'natish` darsi HTML formatda (skrinshot rasmlari bilan) qo'shiladi.
  - Ushbu yangi modul uchun chiquvchi xatlarga doir test savollari (Question va Answer variantlari) kiritiladi.
- **VERIFY**: `seed_lessons.py` kodi sintaktik jihatdan to'g'riligini ruff va django check orqali tekshirish.

### Task 3: Seeding-ni amalga oshirish va tekshirish
- **Agent**: `database-architect`
- **Skills**: `database-design`
- **Priority**: High
- **Dependencies**: Task 2
- **INPUT**: Yangilangan `seed_lessons.py`.
- **OUTPUT**: Ma'lumotlar omboriga (db.sqlite3) yangi modul, dars va testlarning yozilishi.
- **VERIFY**: `.venv\Scripts\python.exe seed_lessons.py` skriptini ishga tushirish va u "Database seeding yakunlandi!" deb muvaffaqiyatli tugashini tekshirish.

---

## Phase X: Verification
- [ ] Lint & Format: `ruff check .` va `ruff format .` buyruqlarini ishga tushirish.
- [ ] Django Migrations & check: `.venv\Scripts\python.exe manage.py check` buyrug'ini tekshirish.
- [ ] Unit & Integration Tests: `pytest` buyrug'ini ishga tushirish va barcha testlar (shu jumladan yangi qo'shilgan model testlari) muvaffaqiyatli o'tishini tekshirish.
- [ ] Manual verification: Mahalliy serverni ishga tushirish va brauzer orqali darslar va testlar to'g'ri integratsiya bo'lganini ko'rish.
