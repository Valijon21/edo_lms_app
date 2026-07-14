# edo_app — Ijro.uz o'quv platformasi

Yangi ishga kirgan xodimlarga **Ijro.uz** tizimida ishlashni o'rgatuvchi web-tizim.
Django backend (kerak bo'lganda Django REST Framework) asosida quriladi.

## Imkoniyatlar
- Kurslar, modullar va darslar (matn, skrinshot, video)
- Oddiy variantli testlar va avtomatik baholash
- O'zlashtirishni kuzatish (progress) va sertifikat
- Rollar: ijrochi, nazoratchi, rahbar
- Rahbar uchun statistika paneli

## Texnologiyalar
- Django 5.x, Django REST Framework
- PostgreSQL (dev: SQLite)
- Django Templates + Bootstrap, test qismida AJAX
- Docker, Gunicorn, Nginx
- GitLab CI

## Loyiha strukturasi
```
config/      # Django sozlamalari
accounts/    # Foydalanuvchi va rollar
courses/     # Kurs, modul, dars
quizzes/     # Test savollari va baholash
progress/    # O'zlashtirish va sertifikat
api/         # DRF endpoint'lari
tests/       # Testlar
```

## Ishga tushirish (dev)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Admin panel: http://127.0.0.1:8000/admin/
API health: http://127.0.0.1:8000/api/health/
