import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from courses.models import Course, Module, Lesson
from quizzes.models import Question, Answer, QuizAttempt


def seed_data():
    print("Database seeding boshlandi...")

    # Eski ma'lumotlarni tozalash (dublikatlarni yo'qotish va toza baza yaratish)
    print("Eski kurslar, modullar, mavzular va testlarni tozalash...")
    from progress.models import Progress
    Progress.objects.all().delete()
    Answer.objects.all().delete()
    Question.objects.all().delete()
    QuizAttempt.objects.all().delete()
    Lesson.objects.all().delete()
    Module.objects.all().delete()
    Course.objects.all().delete()

    # ── Kurs ──
    course, created = Course.objects.get_or_create(
        title="Ijro.uz tizimida ishlash bo'yicha boshlang'ich kurs",
        defaults={
            "description": (
                "Yangi xodimlar uchun Ijro.uz (edo.ijro.uz) tizimida hujjatlar bilan ishlash, "
                "rezolyutsiyalar yozish va ijro nazoratini olib borish bo'yicha amaliy qo'llanma. "
                "Edo.ijro.uz O'zbekiston Respublikasi Prezidentining 2023-yil 24-maydagi PF–76-son "
                "Farmoni hamda PQ–162-son Qarori asosida ishlab chiqilgan yagona elektron hujjat "
                "aylanish platformasidir. Tizim Pm.gov.uz, E-qaror va hrm.argos.uz tizimlariga "
                "integratsiya qilingan."
            ),
            "order": 1,
        },
    )
    if created:
        print(f"Yangi kurs yaratildi: {course.title}")
    else:
        course.description = (
            "Yangi xodimlar uchun Ijro.uz (edo.ijro.uz) tizimida hujjatlar bilan ishlash, "
            "rezolyutsiyalar yozish va ijro nazoratini olib borish bo'yicha amaliy qo'llanma. "
            "Edo.ijro.uz O'zbekiston Respublikasi Prezidentining 2023-yil 24-maydagi PF–76-son "
            "Farmoni hamda PQ–162-son Qarori asosida ishlab chiqilgan yagona elektron hujjat "
            "aylanish platformasidir. Tizim Pm.gov.uz, E-qaror va hrm.argos.uz tizimlariga "
            "integratsiya qilingan."
        )
        course.save()
        print(f"Mavjud kurs yuklandi: {course.title}")

    # ── Dars (Module) ──
    module, created = Module.objects.get_or_create(
        course=course,
        title="1-Dars: Hujjatlar bilan ishlash",
        defaults={"order": 1},
    )
    if not created:
        module.title = "1-Dars: Hujjatlar bilan ishlash"
        module.save()
    print(f"Dars: {module.title}")

    # ═══════════════════════════════════════════════════════════════════
    #  MAVZU 1: Kiruvchi hujjatlarni ro'yxatga olish
    # ═══════════════════════════════════════════════════════════════════
    lesson1_content = """<div class="lesson-rich-content">
    <h3 class="fw-bold text-primary mb-3">📄 Devonxonaga kelgan kiruvchi hujjatlarni ro'yxatga olish</h3>
    <p class="text-muted fs-6 mb-4">Edo.ijro.uz tizimida devonxonaga kelgan va ro'yxatdan o'tmagan hujjatlar bilan ishlash bosqichma-bosqich quyidagi tartibda amalga oshiriladi.</p>

    <div class="step-card mb-5 p-4 border rounded-4 bg-light shadow-sm">
        <h5 class="fw-bold text-dark"><span class="badge bg-primary me-2">1-bosqich</span> Tizimga kirish va Devonxona oynasi</h5>
        <p>Tizimning asosiy navigatsiya menyusidan <strong>"Devonxona"</strong> bo'limiga kiriladi. Devonxonada ro'yxatdan o'tmagan barcha kelib tushgan hujjatlar ko'rinadi. Hujjatlarni ro'yxatga olishdan avval ularning ustiga bosib, fayl mazmunini tekshirib olish lozim.</p>
        <img src="/media/courses/lesson_1/frame_010s.jpg" class="img-fluid rounded-4 my-3 shadow-sm border d-block mx-auto" alt="Devonxona oynasi" style="max-height: 400px;">
        <img src="/media/courses/lesson_1/frame_020s.jpg" class="img-fluid rounded-4 my-2 shadow-sm border d-block mx-auto" alt="Hujjatlar ro'yxati" style="max-height: 400px;">
    </div>

    <div class="step-card mb-5 p-4 border rounded-4 bg-light shadow-sm">
        <h5 class="fw-bold text-dark"><span class="badge bg-primary me-2">2-bosqich</span> Hujjatni tekshirish va Rad etish</h5>
        <p>Fayl ichiga kirib, hujjat tashkilotga tegishli yoki tegishli emasligi aniqlanadi. Agarda hujjat tashkilotga tegishli bo'lmasa, <strong>"Rad etish"</strong> tugmasi bosiladi, rad etish sababi yoziladi va saqlanadi. Hujjat ro'yxatdan avtomatik ravishda yo'qoladi.</p>
        <img src="/media/courses/lesson_1/frame_030s.jpg" class="img-fluid rounded-4 my-3 shadow-sm border d-block mx-auto" alt="Hujjatni rad etish" style="max-height: 400px;">
        <img src="/media/courses/lesson_1/frame_040s.jpg" class="img-fluid rounded-4 my-2 shadow-sm border d-block mx-auto" alt="Rad etish oynasi" style="max-height: 400px;">
    </div>

    <div class="step-card mb-5 p-4 border rounded-4 bg-light shadow-sm">
        <h5 class="fw-bold text-dark"><span class="badge bg-primary me-2">3-bosqich</span> Rekvizitlarni to'ldirish va Ro'yxatga olish</h5>
        <p>Hujjat tashkilotga tegishli bo'lsa, <strong>"Ro'yxatga olish"</strong> tugmasi bosiladi. Tizim avtomatik ravishda quyidagilarni to'ldiradi:</p>
        <ul>
            <li>Yuboruvchi tashkilot nomi</li>
            <li>Hujjat turi (xat)</li>
            <li>Yetkazilish usuli (edo.ijro tizim orqali)</li>
        </ul>
        <p>Ro'yxatga olish jurnalini belgilab, <strong>ustxat imzoluvchi rahbar</strong> va <strong>ijrochi xodim</strong> hamda uning telefon raqamini kiritib, <strong>"Saqlash"</strong> tugmasini bosamiz.</p>
        <img src="/media/courses/lesson_1/frame_060s.jpg" class="img-fluid rounded-4 my-3 shadow-sm border d-block mx-auto" alt="Rekvizitlarni to'ldirish" style="max-height: 400px;">
        <img src="/media/courses/lesson_1/frame_080s.jpg" class="img-fluid rounded-4 my-2 shadow-sm border d-block mx-auto" alt="Saqlash" style="max-height: 400px;">
    </div>

    <div class="step-card mb-5 p-4 border rounded-4 bg-light shadow-sm">
        <h5 class="fw-bold text-dark"><span class="badge bg-primary me-2">4-bosqich</span> Saqlangandan so'ng ma'lumotlarni tekshirish</h5>
        <p>Hujjat saqlangandan so'ng, hujjat haqidagi ma'lumotlar to'g'ri ekanligini tekshiramiz. Agarda ma'lumotlar noto'g'ri qayd etilgan bo'lsa, o'ng tomondagi <strong>uch nuqtani</strong> bosib, <strong>"Tahrirlash"</strong> orqali ma'lumotlarni to'g'rilab chiqish mumkin.</p>
        <img src="/media/courses/lesson_1/frame_090s.jpg" class="img-fluid rounded-4 my-3 shadow-sm border d-block mx-auto" alt="Ma'lumotlarni tekshirish" style="max-height: 400px;">
        <img src="/media/courses/lesson_1/frame_100s.jpg" class="img-fluid rounded-4 my-2 shadow-sm border d-block mx-auto" alt="Tahrirlash" style="max-height: 400px;">
    </div>

    <div class="step-card mb-5 p-4 border rounded-4 bg-light shadow-sm">
        <h5 class="fw-bold text-dark"><span class="badge bg-primary me-2">5-bosqich</span> Hujjatga shtamp qo'yish</h5>
        <p>Hujjat saqlangandan so'ng, uning fayliga qayta kiramiz. O'ng tomondagi <strong>"Shtamp"</strong> yorlig'ini tanlaymiz. Tizim tomonidan generatsiya qilingan kiruvchi tartib raqami va sanasi aks etgan shtampni PDF sahifasining pastki qismiga joylashtirib, o'lchamini moslab, saqlab tasdiqlaymiz.</p>
        <img src="/media/courses/lesson_1/frame_120s.jpg" class="img-fluid rounded-4 my-3 shadow-sm border d-block mx-auto" alt="Shtamp yorlig'i" style="max-height: 400px;">
        <img src="/media/courses/lesson_1/frame_130s.jpg" class="img-fluid rounded-4 my-2 shadow-sm border d-block mx-auto" alt="Shtamp joylash" style="max-height: 400px;">
        <img src="/media/courses/lesson_1/frame_140s.jpg" class="img-fluid rounded-4 my-2 shadow-sm border d-block mx-auto" alt="Shtamp tayyor" style="max-height: 400px;">
    </div>

    <div class="step-card mb-4 p-4 border rounded-4 bg-light shadow-sm">
        <h5 class="fw-bold text-dark"><span class="badge bg-primary me-2">6-bosqich</span> Rezolyutsiya (Ustxat) yozish</h5>
        <p><strong>"Sektor fishka"</strong> yoki <strong>"Rezolyutsiya uchun"</strong> bo'limidan kelgan hujjat tanlanadi va <strong>"Rezolyutsiya"</strong> tugmasi bosiladi. Mas'ul ijrochi tanlanib, topshiriq namunasi (masalan, <em>"Ma'lumot uchun"</em>) tanlanadi va saqlanadi. Topshiriq tegishli xodimlarga yetib boradi.</p>
        <img src="/media/courses/lesson_1/frame_180s.jpg" class="img-fluid rounded-4 my-3 shadow-sm border d-block mx-auto" alt="Rezolyutsiya" style="max-height: 400px;">
        <img src="/media/courses/lesson_1/frame_190s.jpg" class="img-fluid rounded-4 my-2 shadow-sm border d-block mx-auto" alt="Ijrochi tanlash" style="max-height: 400px;">
        <img src="/media/courses/lesson_1/frame_200s.jpg" class="img-fluid rounded-4 my-2 shadow-sm border d-block mx-auto" alt="Saqlash" style="max-height: 400px;">
    </div>

    <div class="alert alert-info border-0 rounded-3 shadow-sm mt-4">
        <i class="bi bi-info-circle me-2"></i>
        <strong>Muhim:</strong> Shtamp qo'yilganda kiruvchi tartib raqami va sana tizim tomonidan avtomatik generatsiya qilinadi — qo'lda yozish shart emas.
    </div>
</div>"""

    lesson1, created = Lesson.objects.get_or_create(
        module=module,
        title="Kiruvchi hujjatlarni ro'yxatga olish",
        defaults={
            "content": lesson1_content,
            "video_url": "https://www.youtube.com/watch?v=ihC3TBPWvSg",
            "order": 1,
        },
    )
    if not created:
        lesson1.content = lesson1_content
        lesson1.video_url = "https://www.youtube.com/watch?v=ihC3TBPWvSg"
        lesson1.save()
    print(f"1-mavzu: {lesson1.title}")

    # ═══════════════════════════════════════════════════════════════════
    #  MAVZU 2: Kiruvchi hujjatlarga javob xati kiritish
    # ═══════════════════════════════════════════════════════════════════
    lesson2_content = """<div class="lesson-rich-content">
    <h3 class="fw-bold text-primary mb-3">✉️ Kiruvchi hujjatlarga javob xati kiritish</h3>
    <p class="text-muted fs-6 mb-4">Tizimda kelgan kiruvchi hujjatlarning ijrosini ta'minlash maqsadida javob xatini shakllantirish va jo'natish jarayoni quyidagi bosqichlarda amalga oshiriladi.</p>

    <div class="step-card mb-5 p-4 border rounded-4 bg-light shadow-sm">
        <h5 class="fw-bold text-dark"><span class="badge bg-primary me-2">1-bosqich</span> Topshiriqni tanlash</h5>
        <p>Tizimdagi <strong>"Topshiriqlar"</strong> bo'limidan <strong>"Ijro uchun"</strong> oynasiga kiriladi. Bajarilishi kutilayotgan topshiriq hujjatlaridan biri tanlanib, uning ostidagi <strong>"Javob xati yaratish"</strong> tugmasi bosiladi.</p>
        <img src="/media/courses/javob_xati_yaratish/frame_010s.jpg" class="img-fluid rounded-4 my-3 shadow-sm border d-block mx-auto" alt="Topshiriqni tanlash" style="max-height: 400px;">
        <img src="/media/courses/javob_xati_yaratish/frame_020s.jpg" class="img-fluid rounded-4 my-2 shadow-sm border d-block mx-auto" alt="Ijro uchun" style="max-height: 400px;">
    </div>

    <div class="step-card mb-5 p-4 border rounded-4 bg-light shadow-sm">
        <h5 class="fw-bold text-dark"><span class="badge bg-primary me-2">2-bosqich</span> Blankani tanlash va muharrirni ochish</h5>
        <p>Javob xati oynasida tegishli <strong>javob xati jurnali</strong> va <strong>blankasi</strong> tanlanadi. So'ngra o'ng tomondagi <strong>"Tahrirlash"</strong> (edit) tugmasi bosilib, rasmiy blankaning onlayn Word muharriri ishga tushiriladi.</p>
        <img src="/media/courses/javob_xati_yaratish/frame_040s.jpg" class="img-fluid rounded-4 my-3 shadow-sm border d-block mx-auto" alt="Blanka tanlash" style="max-height: 400px;">
        <img src="/media/courses/javob_xati_yaratish/frame_050s.jpg" class="img-fluid rounded-4 my-2 shadow-sm border d-block mx-auto" alt="Word muharriri" style="max-height: 400px;">
    </div>

    <div class="step-card mb-5 p-4 border rounded-4 bg-light shadow-sm">
        <h5 class="fw-bold text-dark"><span class="badge bg-primary me-2">3-bosqich</span> Matn kiritish va saqlash</h5>
        <p>Word muharriri ochilgach, javob matnini bevosita shu yerda yozish yoki kompyuterdagi Microsoft Word dasturida oldindan yozib olingan matndan nusxa olib, onlayn muharrirga <strong>Ctrl + V</strong> yordamida joylashtirish mumkin. So'ngra <strong>"Saqlash"</strong> tugmasi bosiladi — hujjat PDF formatiga aylanadi.</p>
        <img src="/media/courses/javob_xati_yaratish/frame_060s.jpg" class="img-fluid rounded-4 my-3 shadow-sm border d-block mx-auto" alt="Matn nusxalash" style="max-height: 400px;">
        <img src="/media/courses/javob_xati_yaratish/frame_080s.jpg" class="img-fluid rounded-4 my-2 shadow-sm border d-block mx-auto" alt="Saqlash" style="max-height: 400px;">
    </div>

    <div class="step-card mb-5 p-4 border rounded-4 bg-light shadow-sm">
        <h5 class="fw-bold text-dark"><span class="badge bg-primary me-2">4-bosqich</span> Ilovalarni biriktirish va Qisqa mazmun</h5>
        <p><strong>Qisqa mazmuni</strong> maydoniga javob xatining qisqacha tavsifi kiritiladi. Agar javob xatiga qo'shimcha tasdiqlovchi yoki yordamchi hujjatlar (ilova) bo'lsa, <strong>"Ilovalar"</strong> bo'limi orqali kompyuterdan fayl yuklanadi.</p>
        <img src="/media/courses/javob_xati_yaratish/frame_100s.jpg" class="img-fluid rounded-4 my-3 shadow-sm border d-block mx-auto" alt="Qisqa mazmun" style="max-height: 400px;">
        <img src="/media/courses/javob_xati_yaratish/frame_120s.jpg" class="img-fluid rounded-4 my-2 shadow-sm border d-block mx-auto" alt="Ilovalar yuklash" style="max-height: 400px;">
    </div>

    <div class="step-card mb-4 p-4 border rounded-4 bg-light shadow-sm">
        <h5 class="fw-bold text-dark"><span class="badge bg-primary me-2">5-bosqich</span> Qabul qiluvchini tanlash va Jo'natish</h5>
        <p>Oxirgi bosqichda javob xatini qabul qiluvchi tashkilot yoki vazirlik tanlanadi. Agar hujjat ichki kelishuvdan o'tishi kerak bo'lsa <strong>"Kelishish uchun"</strong>, to'g'ridan-to'g'ri imzoga chiqadigan bo'lsa <strong>"Imzolash uchun"</strong> mas'ul shaxs tanlanadi va <strong>"Saqlash (Jo'natish)"</strong> tugmasi bosiladi.</p>
        <img src="/media/courses/javob_xati_yaratish/frame_130s.jpg" class="img-fluid rounded-4 my-3 shadow-sm border d-block mx-auto" alt="Qabul qiluvchi" style="max-height: 400px;">
        <img src="/media/courses/javob_xati_yaratish/frame_150s.jpg" class="img-fluid rounded-4 my-2 shadow-sm border d-block mx-auto" alt="Hujjatni jo'natish" style="max-height: 400px;">
    </div>

    <div class="alert alert-info border-0 rounded-3 shadow-sm mt-4">
        <i class="bi bi-info-circle me-2"></i>
        <strong>Muhim:</strong> Word muharriri saqlangandan so'ng, hujjat avtomatik ravishda PDF formatiga o'tkaziladi. PDF holatdagi hujjat rasmiy hujjat sifatida yuboriladi.
    </div>
</div>"""

    lesson2, created = Lesson.objects.get_or_create(
        module=module,
        title="Kiruvchi hujjatlarga javob xati kiritish",
        defaults={
            "content": lesson2_content,
            "video_url": "https://www.youtube.com/watch?v=DObksmEm5WQ",
            "order": 2,
        },
    )
    if not created:
        lesson2.content = lesson2_content
        lesson2.video_url = "https://www.youtube.com/watch?v=DObksmEm5WQ"
        lesson2.save()
    print(f"2-mavzu: {lesson2.title}")

    # ═══════════════════════════════════════════════════════════════════
    #  MAVZU 3: Chiquvchi xatlarni yaratish va jo'natish
    # ═══════════════════════════════════════════════════════════════════
    lesson3_content = """<div class="lesson-rich-content">
    <h3 class="fw-bold text-primary mb-3">📤 Chiquvchi xatlarni yaratish va jo'natish</h3>
    <p class="text-muted fs-6 mb-4">Tizimda yangi chiquvchi xatlarni tayyorlash, ularning matnini tahrirlash hamda imzolash va jo'natish jarayoni quyidagi bosqichlarda amalga oshiriladi.</p>

    <div class="step-card mb-5 p-4 border rounded-4 bg-light shadow-sm">
        <h5 class="fw-bold text-dark"><span class="badge bg-primary me-2">1-bosqich</span> Yangi chiquvchi xat loyihasini yaratish</h5>
        <p>Tizimga kirib, chap tomondagi menyudan <strong>"Chiquvchi"</strong> bo'limi tanlanadi va yuqoridagi <strong>"Yangi yaratish"</strong> tugmasi bosiladi. Chiquvchi xat jurnali va xatning turi (masalan, xat) tanlanadi.</p>
        <img src="/media/courses/chiquvchi_xatlar/frame_010s.jpg" class="img-fluid rounded-4 my-3 shadow-sm border d-block mx-auto" alt="Yangi chiquvchi xat" style="max-height: 400px;">
        <img src="/media/courses/chiquvchi_xatlar/frame_020s.jpg" class="img-fluid rounded-4 my-2 shadow-sm border d-block mx-auto" alt="Xat turi tanlash" style="max-height: 400px;">
    </div>

    <div class="step-card mb-5 p-4 border rounded-4 bg-light shadow-sm">
        <h5 class="fw-bold text-dark"><span class="badge bg-primary me-2">2-bosqich</span> Blankani tanlash va tahrirlash</h5>
        <p>Chiquvchi xat oynasida tegishli rasmiy <strong>blanka turi</strong> tanlanadi. Blankani tahrirlash uchun onlayn Word tahrirchisini ochadigan <strong>"Tahrirlash"</strong> tugmasi bosiladi.</p>
        <img src="/media/courses/chiquvchi_xatlar/frame_040s.jpg" class="img-fluid rounded-4 my-3 shadow-sm border d-block mx-auto" alt="Blanka tanlash" style="max-height: 400px;">
        <img src="/media/courses/chiquvchi_xatlar/frame_050s.jpg" class="img-fluid rounded-4 my-2 shadow-sm border d-block mx-auto" alt="Tahrirlash" style="max-height: 400px;">
    </div>

    <div class="step-card mb-5 p-4 border rounded-4 bg-light shadow-sm">
        <h5 class="fw-bold text-dark"><span class="badge bg-primary me-2">3-bosqich</span> Xat matnini yozish va saqlash</h5>
        <p>Word tahrirchisida rasmiy xat matni yoziladi yoki kompyuterdagi Word dasturidan <strong>Ctrl + V</strong> yordamida nusxa ko'chirilib joylashtiriladi va <strong>"Saqlash"</strong> tugmasi bosiladi. Hujjat PDF formatiga o'tkaziladi.</p>
        <img src="/media/courses/chiquvchi_xatlar/frame_060s.jpg" class="img-fluid rounded-4 my-3 shadow-sm border d-block mx-auto" alt="Matn yozish" style="max-height: 400px;">
        <img src="/media/courses/chiquvchi_xatlar/frame_080s.jpg" class="img-fluid rounded-4 my-2 shadow-sm border d-block mx-auto" alt="PDF formatga o'tkazish" style="max-height: 400px;">
    </div>

    <div class="step-card mb-5 p-4 border rounded-4 bg-light shadow-sm">
        <h5 class="fw-bold text-dark"><span class="badge bg-primary me-2">4-bosqich</span> Qabul qiluvchini tanlash va ilovalarni yuklash</h5>
        <p>Xatning <strong>qisqa mazmuni</strong> maydoni to'ldiriladi va zarur bo'lsa ilova hujjatlari biriktiriladi. <strong>Qabul qiluvchi</strong> qismidan xat yuborilishi kerak bo'lgan tashkilot yoki vazirlik qidirib tanlanadi.</p>
        <img src="/media/courses/chiquvchi_xatlar/frame_100s.jpg" class="img-fluid rounded-4 my-3 shadow-sm border d-block mx-auto" alt="Qabul qiluvchi" style="max-height: 400px;">
        <img src="/media/courses/chiquvchi_xatlar/frame_130s.jpg" class="img-fluid rounded-4 my-2 shadow-sm border d-block mx-auto" alt="Ilovalar" style="max-height: 400px;">
    </div>

    <div class="step-card mb-4 p-4 border rounded-4 bg-light shadow-sm">
        <h5 class="fw-bold text-dark"><span class="badge bg-primary me-2">5-bosqich</span> Kelishuvchilarni belgilash va Imzoga yuborish</h5>
        <p>Agar xat ichki kelishuvdan o'tishi zarur bo'lsa, <strong>kelishuvchi xodimlar</strong> tanlanadi. So'ngra imzolaydigan rahbar mas'ul shaxs sifatida tanlanib, <strong>"Tasdiqlash (Jo'natish)"</strong> tugmasi orqali imzoga yuboriladi.</p>
        <img src="/media/courses/chiquvchi_xatlar/frame_150s.jpg" class="img-fluid rounded-4 my-3 shadow-sm border d-block mx-auto" alt="Kelishuvchilar" style="max-height: 400px;">
        <img src="/media/courses/chiquvchi_xatlar/frame_190s.jpg" class="img-fluid rounded-4 my-2 shadow-sm border d-block mx-auto" alt="Imzoga yuborish" style="max-height: 400px;">
    </div>

    <div class="alert alert-info border-0 rounded-3 shadow-sm mt-4">
        <i class="bi bi-info-circle me-2"></i>
        <strong>Muhim:</strong> Chiquvchi xat imzolangach avtomatik tarzda qabul qiluvchi tashkilotga yetib boradi. Xat raqami va sanasi tizim tomonidan generatsiya qilinadi.
    </div>
</div>"""

    lesson3, created = Lesson.objects.get_or_create(
        module=module,
        title="Chiquvchi xatlarni yaratish va jo'natish",
        defaults={
            "content": lesson3_content,
            "video_url": "",
            "order": 3,
        },
    )
    if not created:
        lesson3.content = lesson3_content
        lesson3.save()
    print(f"3-mavzu: {lesson3.title}")

    # ═══════════════════════════════════════════════════════════════════
    #  MAVZU 4: Ichki buyruqlarni tayyorlash va imzolash
    # ═══════════════════════════════════════════════════════════════════
    lesson4_content = """<div class="lesson-rich-content">
    <h3 class="fw-bold text-primary mb-3">📜 Ichki buyruqlarni tayyorlash va imzolash</h3>
    <p class="text-muted fs-6 mb-4">Tizimda yangi ichki buyruqlarni rasmiylashtirish, ularning loyihasini kelishuvga yuborish va elektron raqamli imzo (ERI) bilan tasdiqlash jarayoni quyidagi bosqichlarda amalga oshiriladi.</p>

    <div class="step-card mb-5 p-4 border rounded-4 bg-light shadow-sm">
        <h5 class="fw-bold text-dark"><span class="badge bg-primary me-2">1-bosqich</span> Yangi buyruq loyihasini yaratish</h5>
        <p>Tizimning bosh navigatsiya menyusidan <strong>"Ichki hujjatlar"</strong> bo'limiga kiriladi. Yangi buyruq loyihasini yaratish uchun <strong>"Yaratish"</strong> (yoki "+") tugmasini bosib, hujjat turidan <strong>"Buyruq"</strong> bandini tanlaymiz. Ro'yxatga olish jurnalida tashkilotning ichki faoliyatiga doir jurnal turini tanlaymiz.</p>
        <img src="/media/courses/ichki_buyruqlar/frame_000s.jpg" class="img-fluid rounded-4 my-3 shadow-sm border d-block mx-auto" alt="Bosh sahifa" style="max-height: 400px;">
        <img src="/media/courses/ichki_buyruqlar/frame_020s.jpg" class="img-fluid rounded-4 my-2 shadow-sm border d-block mx-auto" alt="Ichki hujjatlar" style="max-height: 400px;">
        <img src="/media/courses/ichki_buyruqlar/frame_030s.jpg" class="img-fluid rounded-4 my-2 shadow-sm border d-block mx-auto" alt="Buyruq turi" style="max-height: 400px;">
    </div>

    <div class="step-card mb-5 p-4 border rounded-4 bg-light shadow-sm">
        <h5 class="fw-bold text-dark"><span class="badge bg-primary me-2">2-bosqich</span> Blankani ochish va onlayn muharrir</h5>
        <p>Tizimda buyruq blankasi tayyor holatda joylangan. O'ng tomonda joylashgan <strong>"Tahrirlash"</strong> tugmasini bosamiz. Shunda tizim tomonidan taqdim etilgan <strong>onlayn Word muharriri</strong> ishga tushadi.</p>
        <img src="/media/courses/ichki_buyruqlar/frame_040s.jpg" class="img-fluid rounded-4 my-3 shadow-sm border d-block mx-auto" alt="Tahrirlash tugmasi" style="max-height: 400px;">
        <img src="/media/courses/ichki_buyruqlar/frame_050s.jpg" class="img-fluid rounded-4 my-2 shadow-sm border d-block mx-auto" alt="Word muharriri" style="max-height: 400px;">
    </div>

    <div class="step-card mb-5 p-4 border rounded-4 bg-light shadow-sm">
        <h5 class="fw-bold text-dark"><span class="badge bg-primary me-2">3-bosqich</span> Buyruq matnini yozish va saqlash</h5>
        <p>Word tahrirchisida buyruq matnini bevosita kiritish yoki Microsoft Word dasturidan <strong>Ctrl + V</strong> yordamida nusxa olish orqali joylashtirish mumkin. Agar buyruqning ilovasi bo'lsa (masalan, jadval), uni buyruq matnining ostiga joylashtiramiz. Hujjat matnini saqlab, tahrirlash oynasini yopamiz — hujjat PDF formatiga aylanadi.</p>
        <img src="/media/courses/ichki_buyruqlar/frame_080s.jpg" class="img-fluid rounded-4 my-3 shadow-sm border d-block mx-auto" alt="Buyruq matni" style="max-height: 400px;">
        <img src="/media/courses/ichki_buyruqlar/frame_100s.jpg" class="img-fluid rounded-4 my-2 shadow-sm border d-block mx-auto" alt="Ilova joylash" style="max-height: 400px;">
    </div>

    <div class="step-card mb-5 p-4 border rounded-4 bg-light shadow-sm">
        <h5 class="fw-bold text-dark"><span class="badge bg-primary me-2">4-bosqich</span> Rekvizitlarni to'ldirish va Kelishuvchilarni belgilash</h5>
        <p>Buyruq rekvizitlarini (nomi, qisqa mazmuni, sanasi va h.k.) kiritamiz. Loyihani tasdiqlashda ishtirok etishi kerak bo'lgan mas'ul xodimlarni <strong>"Kelishuvchilar"</strong> ro'yxatiga tizim orqali qidirib qo'shamiz.</p>
        <img src="/media/courses/ichki_buyruqlar/frame_120s.jpg" class="img-fluid rounded-4 my-3 shadow-sm border d-block mx-auto" alt="Rekvizitlar" style="max-height: 400px;">
        <img src="/media/courses/ichki_buyruqlar/frame_130s.jpg" class="img-fluid rounded-4 my-2 shadow-sm border d-block mx-auto" alt="Kelishuvchilar" style="max-height: 400px;">
    </div>

    <div class="step-card mb-4 p-4 border rounded-4 bg-light shadow-sm">
        <h5 class="fw-bold text-dark"><span class="badge bg-primary me-2">5-bosqich</span> Rahbariyatni tanlash va Kelishishga yuborish</h5>
        <p>Oxirgi bosqichda hujjat loyihasini tasdiqlaydigan (imzolaydigan) <strong>rahbar</strong> belgilandi va <strong>"Kelishishga (Imzoga) yuborish"</strong> tugmasi bosiladi. Kelishuvchilar tasdiqlashni amalga oshirganidan so'ng rahbar <strong>ERI (Elektron raqamli imzo) kaliti</strong> orqali buyruqni imzolaydi.</p>
        <img src="/media/courses/ichki_buyruqlar/frame_150s.jpg" class="img-fluid rounded-4 my-3 shadow-sm border d-block mx-auto" alt="Rahbar tanlash" style="max-height: 400px;">
        <img src="/media/courses/ichki_buyruqlar/frame_160s.jpg" class="img-fluid rounded-4 my-2 shadow-sm border d-block mx-auto" alt="Imzoga yuborish" style="max-height: 400px;">
    </div>

    <div class="alert alert-info border-0 rounded-3 shadow-sm mt-4">
        <i class="bi bi-info-circle me-2"></i>
        <strong>Muhim:</strong> ERI kaliti — bu elektron raqamli imzo bo'lib, hujjatning yuridik kuchga ega bo'lishini ta'minlaydi. Kaliti bo'lmagan shaxs buyruqni imzolay olmaydi.
    </div>
</div>"""

    lesson4, created = Lesson.objects.get_or_create(
        module=module,
        title="Ichki buyruqlarni tayyorlash va imzolash",
        defaults={
            "content": lesson4_content,
            "video_url": "",
            "order": 4,
        },
    )
    if not created:
        lesson4.content = lesson4_content
        lesson4.save()
    print(f"4-mavzu: {lesson4.title}")

    # ═══════════════════════════════════════════════════════════════════
    #  SAVOLLAR — har bir mavzu uchun 20 ta (jami 80 ta)
    # ═══════════════════════════════════════════════════════════════════
    # Eski savollarni tozalaymiz
    module.questions.all().delete()
    print("Eski savollar tozalandi. Yangi 80 ta savol yozilmoqda...")

    def make_q(mod, les, text, answers):
        """Yordam funksiyasi: savol va javob variantlarini yaratadi."""
        q = Question.objects.create(module=mod, lesson=les, text=text)
        for ans_text, correct in answers:
            Answer.objects.create(question=q, text=ans_text, is_correct=correct)
        return q

    # ─── 1-Mavzu savollari (20 ta): Kiruvchi hujjatlarni ro'yxatga olish ───
    make_q(module, lesson1, "Kiruvchi hujjatlarni ro'yxatga olish uchun tizimning qaysi bo'limiga kiriladi?",
        [("Devonxona", True), ("Chiquvchi", False), ("Ichki hujjatlar", False), ("Sozlamalar", False)])
    make_q(module, lesson1, "Devonxonaga kelgan hujjat tashkilotga tegishli bo'lmasa nima qilinadi?",
        [("Shtamp qo'yiladi", False), ("To'g'ridan-to'g'ri ijrochiga yuboriladi", False), ("Rad etish tugmasi bosilib, sababi yozilgan holda saqlanadi", True), ("O'chirib yuboriladi", False)])
    make_q(module, lesson1, "Hujjat rad etilgandan keyin u devonxona ro'yxatida qoladi mi?",
        [("Ha, qoladi", False), ("Yo'q, avtomatik ravishda yo'qoladi", True), ("Arxivga o'tkaziladi", False), ("Qayta tekshirishga yuboriladi", False)])
    make_q(module, lesson1, "Hujjat ro'yxatga olinayotganda tizim qaysi ma'lumotlarni avtomatik to'ldiradi?",
        [("Yuboruvchi tashkilot, hujjat turi va yetkazilish usuli", True), ("Faqat sana", False), ("Faqat raqam", False), ("Hech narsani", False)])
    make_q(module, lesson1, "Ro'yxatga olish jurnali sifatida nimani tanlash kerak?",
        [("Chiquvchi jurnal", False), ("Ichki jurnal", False), ("Kiruvchi (turli tashkilot) jurnali", True), ("Arxiv jurnali", False)])
    make_q(module, lesson1, "Hujjat ro'yxatga olinayotganda ustxat imzoluvchi sifatida kim belgilanadi?",
        [("Ijrochi xodim", False), ("Tashkilot rahbari", True), ("Devonxona xodimi", False), ("Tizim administratori", False)])
    make_q(module, lesson1, "Ijrochining telefon raqami qaysi bosqichda kiritiladi?",
        [("Shtamp qo'yish bosqichida", False), ("Rezolyutsiya yozish bosqichida", False), ("Ro'yxatga olish (rekvizitlarni to'ldirish) bosqichida", True), ("Rad etish bosqichida", False)])
    make_q(module, lesson1, "Hujjat saqlangandan so'ng ma'lumotlarni noto'g'ri qayd etilganligini aniqlab, nima qilish mumkin?",
        [("Hujjatni o'chirib qaytadan yozish", False), ("O'ng tomondagi uch nuqtani bosib, tahrirlash orqali tuzatish", True), ("Admin paneliga murojaat qilish", False), ("Yangi hujjat yaratish", False)])
    make_q(module, lesson1, "Shtamp qo'yish uchun hujjatning qaysi qismiga kiriladi?",
        [("Devonxona bo'limiga", False), ("Hujjat fayliga kirib, o'ng tomondagi 'Shtamp' yorlig'i orqali", True), ("Tizim sozlamalariga", False), ("Chop etish bo'limiga", False)])
    make_q(module, lesson1, "Shtampdagi kiruvchi tartib raqami va sana qanday paydo bo'ladi?",
        [("Qo'lda yoziladi", False), ("Faqat sana qo'lda, raqam avtomatik", False), ("Tizim tomonidan avtomatik generatsiya qilinadi", True), ("Rahbar tomonidan belgilanadi", False)])
    make_q(module, lesson1, "Shtampni PDF sahifasining qaysi qismiga joylash tavsiya etiladi?",
        [("Yuqori qism", False), ("Pastki qism", True), ("O'rta qism", False), ("Faqat birinchi sahifaga", False)])
    make_q(module, lesson1, "Shtamp qo'yilgandan so'ng uni tasdiqlash uchun qaysi tugma bosiladi?",
        [("Chiqish", False), ("Saqlash va Tasdiqlash", True), ("Bekor qilish", False), ("Tahrirlash", False)])
    make_q(module, lesson1, "Rezolyutsiya (ustxat) yozish uchun qaysi bo'limga kiriladi?",
        [("Sektor fishka yoki Rezolyutsiya uchun bo'limiga", True), ("Tizim sozlamalari bo'limiga", False), ("Mening profillarim bo'limiga", False), ("Hisobotlar bo'limiga", False)])
    make_q(module, lesson1, "Rezolyutsiya yozishda mas'ul ijrochini tanlash nima uchun zarur?",
        [("Hujjatni arxivlash uchun", False), ("Topshiriq tegishli xodimga yetib borishi uchun", True), ("Shtamp qo'yish uchun", False), ("Blanka tanlash uchun", False)])
    make_q(module, lesson1, "Topshiriq namunalaridan biri qaysi?",
        [("PDF yaratish", False), ("Ma'lumot uchun", True), ("Shtamp qo'yish", False), ("Blanka ochish", False)])
    make_q(module, lesson1, "Hujjatni ro'yxatga olish jarayonida yetkazilish usuli qanday belgilanadi?",
        [("Pochta orqali", False), ("Faks orqali", False), ("Edo.ijro tizim orqali (avtomatik)", True), ("Qo'lda tanlash kerak", False)])
    make_q(module, lesson1, "Shtamp qo'yilgandan so'ng generatsiya raqami nima uchun kerak?",
        [("Hujjatni arxivlash uchun", False), ("Hujjatning yagona identifikatori bo'lib, uni tezda topish uchun", True), ("Faqat hisobot uchun", False), ("Zarur emas", False)])
    make_q(module, lesson1, "Devonxonada ro'yxatdan o'tmagan hujjatlarni ko'rish uchun nima qilish kerak?",
        [("Arxiv bo'limiga kirish", False), ("Devonxona bo'limini ochish", True), ("Topshiriqlar bo'limiga kirish", False), ("Sozlamalarga o'tish", False)])
    make_q(module, lesson1, "Hujjat ro'yxatga olinganidan so'ng unga qaysi raqam beriladi?",
        [("Chiquvchi raqam", False), ("Kiruvchi tartib raqami (tizim tomonidan avtomatik)", True), ("Ichki buyruq raqami", False), ("Raqam berilmaydi", False)])
    make_q(module, lesson1, "Rezolyutsiya saqlangandan so'ng topshiriq qayerga yetib boradi?",
        [("Arxivga", False), ("Devonxonaga", False), ("Belgilangan ijrochi xodimga", True), ("Tizim administratoriga", False)])

    # ─── 2-Mavzu savollari (20 ta): Kiruvchi hujjatlarga javob xati kiritish ───
    make_q(module, lesson2, "Kiruvchi hujjatga javob xati yozish uchun birinchi navbatda qaysi bo'limga kiriladi?",
        [("Tizim sozlamalari", False), ("Topshiriqlar -> Ijro uchun bo'limiga kirib, tegishli hujjat tanlanadi", True), ("Xodimlar bazasi", False), ("Hisobotlar bo'limiga", False)])
    make_q(module, lesson2, "Javob xati yaratish tugmasi qayerda joylashgan?",
        [("Devonxona bo'limida", False), ("Topshiriq hujjatining ostida", True), ("Tizim sozlamalarida", False), ("Bosh sahifada", False)])
    make_q(module, lesson2, "Javob xati uchun blanka nima?",
        [("Bo'sh qog'oz", False), ("Tashkilotning rasmiy hujjat shakli (gerb, sarlavha va h.k.)", True), ("PDF fayl", False), ("Skaner qilingan rasm", False)])
    make_q(module, lesson2, "Blankani tahrirlash uchun qaysi tugma bosiladi?",
        [("Yuklash", False), ("Tahrirlash (onlayn Word muharriri)", True), ("Tasdiqlash", False), ("O'chirish", False)])
    make_q(module, lesson2, "Javob xati matnini rasmiy blankaga kiritishning qanday usuli bor?",
        [("Faqat skaner qilingan rasmni yuklash", False), ("Faqat og'zaki tushuntirish", False), ("Tahrirlash tugmasini bosib, Word muharririda yozish yoki Ctrl+V orqali nusxa olish", True), ("Boshqa sayt orqali", False)])
    make_q(module, lesson2, "Word muharririda matn saqlangandan so'ng hujjat qaysi formatga aylanadi?",
        [("Word (.docx)", False), ("PDF (.pdf)", True), ("Rasm (.jpg)", False), ("Excel (.xlsx)", False)])
    make_q(module, lesson2, "Qisqa mazmun maydoni nima uchun kerak?",
        [("Javob xatining qisqacha tavsifi uchun", True), ("Hujjatning to'liq matnini yozish uchun", False), ("Rasm joylash uchun", False), ("Parol kiritish uchun", False)])
    make_q(module, lesson2, "Javob xatiga ilova (qo'shimcha fayl) qanday biriktiriladi?",
        [("Ilovalar bo'limi orqali kompyuterdan fayl yuklanadi", True), ("Faqat matn sifatida yoziladi", False), ("Email orqali yuboriladi", False), ("Ilova biriktirish mumkin emas", False)])
    make_q(module, lesson2, "Qabul qiluvchini tanlash bosqichida nima qilinadi?",
        [("Hujjat o'chiriladi", False), ("Javob xatini qabul qiluvchi tashkilot yoki vazirlik tanlanadi", True), ("Yangi blanka ochiladi", False), ("Shtamp qo'yiladi", False)])
    make_q(module, lesson2, "Javob xati to'g'ridan-to'g'ri imzoga yuborilishi uchun qaysi variantni tanlash kerak?",
        [("Kelishish uchun", False), ("Imzolash uchun", True), ("Rad etish", False), ("Arxivga yuborish", False)])
    make_q(module, lesson2, "Javob xati ichki kelishuvdan o'tishi kerak bo'lsa qaysi variantni tanlash kerak?",
        [("Imzolash uchun", False), ("Kelishish uchun", True), ("Qayta yozish", False), ("Bekor qilish", False)])
    make_q(module, lesson2, "Tayyor javob xatini jo'natish uchun oxirgi tugma qaysi?",
        [("Tahrirlash", False), ("Saqlash (Jo'natish)", True), ("Bekor qilish", False), ("Chiqish", False)])
    make_q(module, lesson2, "Ctrl+V buyrug'i nima uchun ishlatiladi?",
        [("Hujjatni o'chirish uchun", False), ("Oldindan nusxa olingan matnni joylashtirish uchun", True), ("Yangi fayl yaratish uchun", False), ("Chop etish uchun", False)])
    make_q(module, lesson2, "Topshiriqlar bo'limidagi 'Ijro uchun' nima?",
        [("Bajarilishi kutilayotgan hujjatlar ro'yxati", True), ("O'chirilgan hujjatlar", False), ("Arxivdagi hujjatlar", False), ("Yangi yaratilgan hujjatlar", False)])
    make_q(module, lesson2, "Javob xati jurnali nima?",
        [("Javob xatlari uchun belgilangan maxsus jurnal turi", True), ("Kiruvchi hujjatlar jurnali", False), ("Ichki buyruqlar jurnali", False), ("Tizim sozlamalari jurnali", False)])
    make_q(module, lesson2, "Onlayn Word muharriri qaysi tashkilot tomonidan ishlab chiqilgan?",
        [("Microsoft", True), ("Google", False), ("Apple", False), ("Tizim o'zi", False)])
    make_q(module, lesson2, "Ilova fayllari qayerdan yuklanadi?",
        [("Internet brauzerdan", False), ("Kompyuterdan (rabocha stulidan)", True), ("Faqat telefon orqali", False), ("Faqat email orqali", False)])
    make_q(module, lesson2, "Imzolash uchun tanlangan mas'ul shaxs odatda kim bo'ladi?",
        [("Devonxona xodimi", False), ("Rahbar", True), ("Oddiy ijrochi", False), ("Tizim administratori", False)])
    make_q(module, lesson2, "PDF formatdagi hujjat nima uchun rasmiy hisoblandi?",
        [("O'zgartirish qiyin bo'lgani uchun", True), ("Katta hajmda bo'lgani uchun", False), ("Faqat chop etish uchun mo'ljallangani uchun", False), ("Rang-barang bo'lgani uchun", False)])
    make_q(module, lesson2, "Javob xati jo'natilgandan so'ng uni qayta tahrirlash mumkinmi?",
        [("Ha, istalgan vaqt", False), ("Yo'q, imzolangan hujjatni qayta tahrirlash mumkin emas", True), ("Faqat admin qila oladi", False), ("Faqat hafta oxirida", False)])

    # ─── 3-Mavzu savollari (20 ta): Chiquvchi xatlarni yaratish va jo'natish ───
    make_q(module, lesson3, "Chiquvchi xat loyihasini yaratish uchun qaysi bo'limga kiriladi?",
        [("Devonxona", False), ("Chiquvchi bo'limiga kirib, 'Yangi yaratish' tugmasini bosish", True), ("Topshiriqlar", False), ("Arxiv", False)])
    make_q(module, lesson3, "Chiquvchi xat loyihasida blanka matnini tahrirlash uchun qaysi tugma bosiladi?",
        [("Yuklash", False), ("Tahrirlash (onlayn Word muharriri)", True), ("Tasdiqlash", False), ("O'chirish", False)])
    make_q(module, lesson3, "Chiquvchi xat matni saqlangandan so'ng avtomatik qaysi formatga o'tkaziladi?",
        [("Word (.docx)", False), ("PDF (.pdf)", True), ("Rasm (.jpg)", False), ("Excel (.xlsx)", False)])
    make_q(module, lesson3, "Chiquvchi xatning qisqa mazmuni maydoniga nima yoziladi?",
        [("Hujjatning to'liq matni", False), ("Xatning qisqacha tavsifi", True), ("Parol", False), ("Rahbar ismi", False)])
    make_q(module, lesson3, "Chiquvchi xat loyihasiga qo'shimcha hujjatlar biriktirish zarur bo'lsa nima qilinadi?",
        [("Ilovalar bo'limidan fayl yuklanadi", True), ("Email orqali yuboriladi", False), ("Alohida xat yoziladi", False), ("Ilova biriktirish mumkin emas", False)])
    make_q(module, lesson3, "Qabul qiluvchi tashkilot qanday tanlanadi?",
        [("Qidiruv orqali topib tanlanadi", True), ("Qo'lda telefon raqam kiritiladi", False), ("Tizim avtomatik tanlaydi", False), ("Faqat bitta tashkilotga yuborish mumkin", False)])
    make_q(module, lesson3, "Chiquvchi xat loyihasi to'liq tayyor bo'lgandan so'ng kimga yuboriladi?",
        [("Tashqi yuboruvchiga", False), ("Imzolash uchun rahbariyatga yoki kelishuvchi mas'ullarga", True), ("Faqat arxivga", False), ("Hech kimga", False)])
    make_q(module, lesson3, "Kelishuvchi mas'ullar qachon belgilanadi?",
        [("Xat ichki kelishuvdan o'tishi zarur bo'lganda", True), ("Har doim", False), ("Faqat kiruvchi hujjatlarda", False), ("Hech qachon", False)])
    make_q(module, lesson3, "Chiquvchi xat raqami va sanasi qanday generatsiya qilinadi?",
        [("Qo'lda yoziladi", False), ("Rahbar belgilaydi", False), ("Tizim tomonidan avtomatik", True), ("Devonxona xodimi kiritadi", False)])
    make_q(module, lesson3, "Imzolaydigan rahbar sifatida kim tanlanadi?",
        [("Istalgan xodim", False), ("Tashkilot rahbari yoki vakolatli shaxs", True), ("Tizim administratori", False), ("Devonxona boshlig'i", False)])
    make_q(module, lesson3, "Chiquvchi xat imzolangach nima bo'ladi?",
        [("Hujjat o'chiriladi", False), ("Qabul qiluvchi tashkilotga avtomatik yetib boradi", True), ("Arxivga tushadi", False), ("Qayta tahrirlash kerak", False)])
    make_q(module, lesson3, "Chap menyudan 'Chiquvchi' bo'limiga kirganda nima ko'rinadi?",
        [("Devonxona hujjatlari", False), ("Chiquvchi xatlar ro'yxati va 'Yangi yaratish' tugmasi", True), ("Faqat sozlamalar", False), ("Ichki buyruqlar", False)])
    make_q(module, lesson3, "Word tahrirchisida xat matnini kiritishning qanday usullari bor?",
        [("Faqat bevosita yozish", False), ("Bevosita yozish yoki Ctrl+V orqali nusxa joylash", True), ("Faqat skaner qilish", False), ("Faqat ovozli kiritish", False)])
    make_q(module, lesson3, "Chiquvchi xat jurnali nima?",
        [("Chiquvchi xatlar uchun belgilangan maxsus jurnal turi", True), ("Kiruvchi hujjatlar jurnali", False), ("Shaxsiy kundalik", False), ("Hisobot jurnali", False)])
    make_q(module, lesson3, "'Tasdiqlash (Jo'natish)' tugmasi qachon bosiladi?",
        [("Xat blankasi tanlanganida", False), ("Barcha ma'lumotlar to'ldirilgandan va kelishuvchilar belgilangandan so'ng", True), ("Matn yozish boshida", False), ("Tizimga kirganida", False)])
    make_q(module, lesson3, "Chiquvchi xat bilan kiruvchi hujjatga javob xati o'rtasidagi farq nima?",
        [("Farqi yo'q", False), ("Chiquvchi xat mustaqil yaratiladi, javob xati esa mavjud topshiriqqa javoban tayyorlanadi", True), ("Javob xati rasmiy emas", False), ("Chiquvchi xat imzolanmaydi", False)])
    make_q(module, lesson3, "Chiquvchi xat uchun blanka tanlash nima uchun kerak?",
        [("Tashkilotning rasmiy shaklidagi hujjat yaratish uchun", True), ("Faqat chiroyli ko'rinishi uchun", False), ("Tizim talabi emas", False), ("Faqat chop etish uchun", False)])
    make_q(module, lesson3, "Bir nechta qabul qiluvchi tashkilot tanlash mumkinmi?",
        [("Ha, bir nechta tashkilot tanlash mumkin", True), ("Yo'q, faqat bitta", False), ("Faqat ikki dona", False), ("Faqat bir turdagi tashkilotlar", False)])
    make_q(module, lesson3, "Chiquvchi xat PDF formatga o'tgandan so'ng nima qilinadi?",
        [("Matn qayta yoziladi", False), ("Qisqa mazmun, qabul qiluvchi va kelishuvchilar belgilanadi", True), ("Hujjat o'chiriladi", False), ("Yangi blanka yaratiladi", False)])
    make_q(module, lesson3, "Kelishish jarayonida kelishuvchi xodim nimani tekshiradi?",
        [("Hujjatning mazmuni to'g'ri va to'liq ekanligini", True), ("Faqat shtamp bor-yo'qligini", False), ("Faqat sana to'g'riligini", False), ("Hech narsani", False)])

    # ─── 4-Mavzu savollari (20 ta): Ichki buyruqlarni tayyorlash va imzolash ───
    make_q(module, lesson4, "Edo.ijro.uz tizimida yangi ichki buyruq yaratish uchun qaysi bo'limga kiriladi?",
        [("Ichki hujjatlar", True), ("Kiruvchi hujjatlar", False), ("Sozlamalar", False), ("Nazorat paneli", False)])
    make_q(module, lesson4, "Ichki buyruq yaratish uchun hujjat turidan qaysi band tanlanadi?",
        [("Xat", False), ("Buyruq", True), ("Memorandum", False), ("Bayonnoma", False)])
    make_q(module, lesson4, "Ro'yxatga olish jurnalida qaysi jurnal turi tanlanadi?",
        [("Kiruvchi jurnal", False), ("Chiquvchi jurnal", False), ("Tashkilotning ichki faoliyatiga doir jurnal", True), ("Arxiv jurnali", False)])
    make_q(module, lesson4, "Ichki buyruq uchun blanka tizimda qanday holatda?",
        [("Yuklab olish kerak", False), ("Tizimda tayyor holatda joylangan", True), ("Har safar qayta yaratiladi", False), ("Mavjud emas", False)])
    make_q(module, lesson4, "Buyruq blankasini tahrirlash uchun qaysi tugma bosiladi?",
        [("Saqlash", False), ("Tahrirlash (onlayn Word muharriri ochiladi)", True), ("O'chirish", False), ("Yuklash", False)])
    make_q(module, lesson4, "Buyruq matnini kiritishda Ctrl+V nima uchun ishlatiladi?",
        [("Faylni o'chirish uchun", False), ("Oldindan tayyorlab qo'yilgan matnni joylashtirish uchun", True), ("Yangi oyna ochish uchun", False), ("Chop etish uchun", False)])
    make_q(module, lesson4, "Buyruqning ilovasi (masalan, jadval) qayerga joylashtiriladi?",
        [("Buyruq matnining ustiga", False), ("Buyruq matnining ostiga", True), ("Alohida hujjat sifatida", False), ("Ilovalar bo'limiga", False)])
    make_q(module, lesson4, "Buyruq matnini saqlangandan so'ng hujjat qaysi formatga aylanadi?",
        [("Word", False), ("PDF", True), ("Excel", False), ("Rasm", False)])
    make_q(module, lesson4, "Buyruq rekvizitlarida qaysi ma'lumotlar kiritiladi?",
        [("Nomi, qisqa mazmuni, sanasi va h.k.", True), ("Faqat sana", False), ("Faqat raqam", False), ("Hech nima", False)])
    make_q(module, lesson4, "Kelishuvchilar ro'yxatiga kim qo'shiladi?",
        [("Faqat rahbar", False), ("Loyihani tasdiqlashda ishtirok etishi kerak bo'lgan mas'ul xodimlar", True), ("Faqat devonxona xodimi", False), ("Tizim administratori", False)])
    make_q(module, lesson4, "Kelishuvchilarni tizimda qanday topish mumkin?",
        [("Qo'lda yozish kerak", False), ("Tizim orqali qidirib qo'shish", True), ("Faqat admin panel orqali", False), ("Email orqali yuborish", False)])
    make_q(module, lesson4, "Ichki buyruq loyihasini imzolashga yuborishdan avval uni boshqa mas'ullar bilan kelishish shartmi?",
        [("Yo'q, shart emas", False), ("Ha, kelishish uchun 'Kelishuvchilar' ro'yxatiga mas'ul xodimlar qo'shiladi", True), ("Faqat og'zaki kelishiladi", False), ("Buyruqlar kelishilmaydi", False)])
    make_q(module, lesson4, "Kelishuvchilar kelishuvini amalga oshirganidan so'ng nima bo'ladi?",
        [("Hujjat o'chiriladi", False), ("Buyruq tayyor va tasdiqlangan holatda bo'ladi, imzo chekuvchiga jo'natiladi", True), ("Arxivga tushadi", False), ("Qayta yoziladi", False)])
    make_q(module, lesson4, "Tayyor bo'lgan ichki buyruq qanday imzolanadi?",
        [("Qog'ozda qo'lda imzolash orqali", False), ("Rahbar tomonidan tizimda ERI kaliti yordamida imzolash orqali", True), ("Tizim tashqarisida pochta orqali", False), ("Imzo talab etilmaydi", False)])
    make_q(module, lesson4, "ERI kaliti nima?",
        [("Maxfiy parol", False), ("Elektron raqamli imzo — hujjatning yuridik kuchga ega bo'lishini ta'minlaydi", True), ("Tizimga kirish kaliti", False), ("USB flesh-disk", False)])
    make_q(module, lesson4, "ERI kaliti bo'lmagan shaxs buyruqni imzolay oladimi?",
        [("Ha, istalgan vaqt", False), ("Yo'q, ERI kalitisiz imzolash mumkin emas", True), ("Faqat admin ruxsati bilan", False), ("Parol bilan mumkin", False)])
    make_q(module, lesson4, "Ichki buyruq va chiquvchi xat o'rtasidagi asosiy farq nima?",
        [("Farqi yo'q", False), ("Ichki buyruq tashkilot ichida qo'llaniladi, chiquvchi xat tashqi tashkilotga yuboriladi", True), ("Chiquvchi xat imzolanmaydi", False), ("Ichki buyruq imzolanmaydi", False)])
    make_q(module, lesson4, "'Kelishishga (Imzoga) yuborish' tugmasi qachon bosiladi?",
        [("Matn yozish boshida", False), ("Barcha rekvizitlar to'ldirilgandan va kelishuvchilar belgilangandan so'ng", True), ("Tizimga kirganida", False), ("Faqat hafta boshida", False)])
    make_q(module, lesson4, "Ichki buyruq imzolangandan so'ng uni qayta o'zgartirish mumkinmi?",
        [("Ha, istalgan vaqt", False), ("Yo'q, imzolangan hujjat o'zgartirish mumkin emas", True), ("Faqat rahbar o'zgartira oladi", False), ("Faqat bir hafta ichida", False)])
    make_q(module, lesson4, "Buyruq blankasi albom (gorizontal) ko'rinishda bo'lganda uni qanday joylash kerak?",
        [("Faqat vertikal holatda", False), ("Albom ko'rinishda joylashtirish, jadvallarni mos ravishda moslab qo'yish", True), ("Joylashtirib bo'lmaydi", False), ("Faqat skaner orqali", False)])

    print("Success! Barcha 80 ta savol (4 × 20) va javob variantlari muvaffaqiyatli yaratildi.")
    print("Database seeding yakunlandi!")


if __name__ == "__main__":
    seed_data()
